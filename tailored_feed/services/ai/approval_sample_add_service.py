import inspect, os, joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.session.session import Session
from tailored_feed.models.ai.approval_sample import ApprovalSample
from tailored_feed.services.ai.approval_sample_add_service_interface import ApprovalSampleAddServiceInterface

class ApprovalSampleAddService(ApprovalSampleAddServiceInterface):

    def __init__(self, get_repository, add_repository):
        self.exception_manager = ExceptionManager()
        self.get_repository = get_repository
        self.add_repository = add_repository


    def generate_iteration_model(
        self, iteration: int, assessment_id: int, session_student_id: int, session_id: int, 
        question_index_assessed: int, assessment_last_question_index: int
    ):
        try:
            self.handle_approval_samples_addition(
                iteration, assessment_id, session_student_id, 
                question_index_assessed, assessment_last_question_index
            )
            
            self.train_model(assessment_id, session_id, iteration)
            
            session = Session.objects.get(pk=session_id)
            session.approvalModelQuestionIndicesAssessed.append(question_index_assessed)
            session.save()

        except Exception as e:            
            argspec = inspect.getfullargspec(self.generate_iteration_model)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "generate_iteration_model", parameters, str(e))


    def predict_student_approval(
        self, assessment_id, session_id, session_student_id,
        iteration_index_assessed, iteration, assessment_last_question_index
    ):
        try:
            model_dir = "ai_models"
            model_filename = os.path.join(model_dir, f'ml_model_session_{session_id}_iteration_{iteration}.pkl')
            scaler_filename = os.path.join(model_dir, f'scaler_session_{session_id}_iteration_{iteration}.pkl')

            if not os.path.exists(model_filename) or not os.path.exists(scaler_filename):
                return "Error: Model or scaler file not found."
            
            model = joblib.load(model_filename)
            scaler = joblib.load(scaler_filename)
            
            normalized_student_answer = self.get_normalized_student_answers(
                session_student_id, iteration_index_assessed
            )

            # TMP Remove elapse_time and bandwith
            fix_normalized_student_answers = normalized_student_answer.copy()
            del fix_normalized_student_answers["elapsed_time"]
            del fix_normalized_student_answers["bandwidth"]

            df = pd.DataFrame([fix_normalized_student_answers])
            X_scaled = scaler.transform(df)
            prediction = model.predict(X_scaled)[0]
            is_approved = True if prediction == 1 else False
            
            self.add_approval_sample(normalized_student_answer, assessment_id, session_student_id, iteration, True, is_approved)
            
            return "approved" if prediction == 1 else "disapproved"
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.predict_student_approval)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "predict_student_approval", parameters, str(e))


    def handle_approval_samples_addition(
        self, iteration: int, assessment_id: int, session_student_id: int, 
        question_index_assessed: int, assessment_last_question_index: int
    ):
        session_answers = self.get_repository.finished_session_students_answers(
            assessment_id, question_index_assessed, assessment_last_question_index
        )
        
        if not session_answers.exists():
            raise Exception(f'No se encontraron respuesta para procesar.')
        
        session_students = {}
        for answer in session_answers:
            session_students.setdefault(answer.sessionStudent_id, answer.sessionStudent.grade)
        
        for session_student_id, grade in session_students.items():
            student_answers = session_answers.filter(sessionStudent_id=session_student_id)
            is_approved = grade >= 60

            normalized_student_answer = self.normalize_student_answers(student_answers)

            self.add_approval_sample(
                normalized_student_answer, assessment_id, session_student_id, iteration, False, is_approved
            )


    def train_model(self, assessment_id, session_id, iteration):
        try:
            df = self.get_training_data(assessment_id, iteration)
            X = df.drop(columns=['isApproved'])
            X = X[['luminosity', 'noiseLevel', 'correctAnswers']]
            X['correctAnswers'] *= 100
            y = df['isApproved']

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
            
            #model = LogisticRegression()
            model = LogisticRegression(class_weight={0: 30, 1: 1})
            model.fit(X_train, y_train)


            print("PPPPPPPPPPPPPPPPPPPP")
            #feature_names = ["bandwidth", "luminosity", "noiseLevel", "correctAnswers"]
            feature_names = ["luminosity", "noiseLevel", "correctAnswers"]
            importance = model.coef_[0]  # Get the learned weights

            for name, coef in zip(feature_names, importance):
                print(f"Feature: {name}, Weight: {coef:.3f}")

            
            model_dir = "ai_models"
            os.makedirs(model_dir, exist_ok=True)

            model_filename = os.path.join(model_dir, f'ml_model_session_{session_id}_iteration_{iteration}.pkl')
            scaler_filename = os.path.join(model_dir, f'scaler_session_{session_id}_iteration_{iteration}.pkl')
            
            joblib.dump(model, model_filename)
            joblib.dump(scaler, scaler_filename)
            
            return model

        except Exception as e:
            argspec = inspect.getfullargspec(self.train_model)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "train_model", parameters, str(e))


    def add_approval_sample(self, normalized_student_answer, assessment_id, session_student_id, iteration, is_predicted, is_approved):        
        approval_sample = ApprovalSample(
            assessment_id=assessment_id,
            session_student_id=session_student_id,
            iteration=iteration,
            isPredicted=is_predicted,
            isApproved=is_approved,
            bandwidth=normalized_student_answer['bandwidth'],
            luminosity=normalized_student_answer['luminosity'],
            noiseLevel=normalized_student_answer['noiseLevel'],
            correctAnswers=normalized_student_answer['correctAnswers'],
            elapsedTime=normalized_student_answer['elapsed_time']
        )
        
        self.add_repository.add(approval_sample)


    def normalize_student_answers(self, student_answers):
        total_answers = student_answers.count()

        return {
            'bandwidth': sum(ans.userContext.get("bandwidth", 0) for ans in student_answers) / total_answers,
            'luminosity': sum(ans.userContext.get("luminosity", 0) for ans in student_answers) / total_answers,
            'noiseLevel': sum(ans.userContext.get("noiseLevel", 0) for ans in student_answers) / total_answers,
            'correctAnswers': sum(ans.isCorrect for ans in student_answers),
            'elapsed_time': sum(ans.elapsedTime for ans in student_answers) / total_answers
        }


    def get_training_data(self, assessment_id, iteration):
        """
        results = ApprovalSample.objects.filter(
            assessment_id=assessment_id, iteration=iteration, isPredicted=False
        ).values(
            'isApproved', 'bandwidth', 'luminosity', 'noiseLevel', 'correctAnswers', 'elapsedTime'
        )

        # TMP Remove elapse_time
        results = ApprovalSample.objects.filter(
            assessment_id=assessment_id, iteration=iteration, isPredicted=False
        ).values(
            'isApproved', 'bandwidth', 'luminosity', 'noiseLevel', 'correctAnswers'
        )
        """
        # TMP Remove bandwith test
        results = ApprovalSample.objects.filter(
            assessment_id=assessment_id, iteration=iteration, isPredicted=False
        ).values(
            'isApproved', 'luminosity', 'noiseLevel', 'correctAnswers'
        )
        
        df = pd.DataFrame(results)
        df['isApproved'] = df['isApproved'].astype(int)
        
        return df


    def get_normalized_student_answers(
        self, session_student_id, question_index_assessed
    ):
        student_answers = self.get_repository.student_answers_from_index(
            session_student_id, question_index_assessed
        )

        if not student_answers.exists():
            raise Exception(f'No se encontraron respuesta para procesar.')

        return self.normalize_student_answers(student_answers)