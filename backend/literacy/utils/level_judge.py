from literacy.models import LiteracyCriteria

# 문해력 판단 로직
class LiteracyLevelJudge:
    
    def __init__(self):
        # DB에서 모든 기준 데이터 로드
        self.criteria_data = list(LiteracyCriteria.objects.all().order_by('literacy_level'))
    
    def calculate_stage_accuracy(self, test_result, stage):
        """특정 단계의 정답률 계산"""
        stage_questions = test_result.get(f'stage_{stage}', [])
        if not stage_questions:
            return 0
        
        correct_count = sum(1 for answer in stage_questions if answer['is_correct'])
        return correct_count / len(stage_questions)
    
    def calculate_avg_accuracy(self, test_result, stages):
        """여러 단계의 평균 정답률 계산"""
        accuracies = [self.calculate_stage_accuracy(test_result, stage) for stage in stages]
        return sum(accuracies) / len(accuracies) if accuracies else 0
    
    def count_correct_answers(self, test_result, stage):
        """특정 단계의 정답 개수 계산"""
        stage_questions = test_result.get(f'stage_{stage}', [])
        return sum(1 for answer in stage_questions if answer['is_correct'])
    
    def count_incorrect_answers(self, test_result, stage):
        """특정 단계의 오답 개수 계산"""
        stage_questions = test_result.get(f'stage_{stage}', [])
        return sum(1 for answer in stage_questions if not answer['is_correct'])
    
    def calculate_total_score(self, test_result):
        """전체 정답 개수 계산"""
        total_correct = 0
        for stage in range(1, 6):  # 1~5단계
            stage_questions = test_result.get(f'stage_{stage}', [])
            total_correct += sum(1 for answer in stage_questions if answer['is_correct'])
        return total_correct
    
    def evaluate_condition(self, test_result, stage_key, condition):
        """개별 조건 평가"""
        operator = condition['operator']
        value = condition['value']
        comparison = condition['comparison']
        
        if operator == 'accuracy':
            stage_num = int(stage_key.split('_')[1])
            actual_value = self.calculate_stage_accuracy(test_result, stage_num)
        elif operator == 'avg_accuracy':
            stages = condition['stages']
            actual_value = self.calculate_avg_accuracy(test_result, stages)
        elif operator == 'correct_count':
            stage_num = int(stage_key.split('_')[1])
            actual_value = self.count_correct_answers(test_result, stage_num)
        elif operator == 'incorrect_count':
            stage_num = int(stage_key.split('_')[1])
            actual_value = self.count_incorrect_answers(test_result, stage_num)
        else:
            return False
        
        # 비교 연산 수행
        if comparison == '>=':
            return actual_value >= value
        elif comparison == '<=':
            return actual_value <= value
        elif comparison == '>':
            return actual_value > value
        elif comparison == '<':
            return actual_value < value
        elif comparison == '==':
            return actual_value == value
        
        return False
    
    def check_criteria(self, test_result, criteria_obj):
        """기준 조건 체크"""
        level_criteria = criteria_obj.level_criteria
        
        # 총점 체크
        total = self.calculate_total_score(test_result)
        total_score = level_criteria['total_score']
        if not (total_score['min'] <= total <= total_score['max']):
            return False
        
        # 단계별 정확도 체크
        if 'stage_accuracy' in level_criteria:
            for stage_key, condition in level_criteria['stage_accuracy'].items():
                if not self.evaluate_condition(test_result, stage_key, condition):
                    return False
        
        return True
    
    def check_exception_criteria(self, test_result, criteria_obj):
        """예외 조건 체크"""
        if not criteria_obj.exception_allowed:
            return False
        
        exception = criteria_obj.exception_allowed
        
        # 총점 예외 체크
        if 'total_score' in exception:
            total = self.calculate_total_score(test_result)
            total_exception = exception['total_score']
            if not (total_exception['min'] <= total <= total_exception['max']):
                return False
        
        # 단계별 예외 조건 체크
        if 'stage_accuracy' in exception:
            for stage_key, condition in exception['stage_accuracy'].items():
                if not self.evaluate_condition(test_result, stage_key, condition):
                    return False
        
        return True
    
    def judge_literacy_level(self, test_result):
        """
        테스트 결과를 바탕으로 문해력 수준 판단
        
        Args:
            test_result (dict): {
                'stage_1': [{'question_id': 1, 'is_correct': True}, ...],
                'stage_2': [{'question_id': 2, 'is_correct': False}, ...],
                ...
            }
        
        Returns:
            dict: {
                'literacy_level': int,
                'feedback': str,
                'recommendation': str,
                'is_exception': bool,
                'debug_info': dict
            }
        """
        
        debug_info = {
            'total_score': self.calculate_total_score(test_result),
            'stage_accuracies': {}
        }
        
        correct = debug_info['total_score']
        total_q = 15

        
        # 각 단계별 정답률 계산 (디버깅용)
        for stage in range(1, 6):
            debug_info['stage_accuracies'][f'stage_{stage}'] = self.calculate_stage_accuracy(test_result, stage)
        
        # 우선순위에 따라 순차적으로 체크 (레벨 1이 최우선)
        for criteria_obj in self.criteria_data:
            # 정규 기준 체크
            if self.check_criteria(test_result, criteria_obj):
                return {
                    'literacy_level': criteria_obj.literacy_level,
                    'feedback': criteria_obj.feedback,
                    'recommendation': criteria_obj.recommendation,
                    'is_exception': False,
                    'correct_answers': correct,
                    'total_questions': total_q,
                    'debug_info': debug_info
                }
            
            # 예외 조건 체크
            if self.check_exception_criteria(test_result, criteria_obj):
                return {
                    'literacy_level': criteria_obj.literacy_level,
                    'feedback': criteria_obj.feedback,
                    'recommendation': criteria_obj.recommendation,
                    'is_exception': True,                    
                    'correct_answers': correct,
                    'total_questions': total_q,
                    'debug_info': debug_info
                }
        
        # 어떤 기준에도 맞지 않는 경우 (기본값: 레벨 1)
        default_criteria = self.criteria_data[0] if self.criteria_data else None
        if default_criteria:
            return {
                'literacy_level': default_criteria.literacy_level,
                'feedback': default_criteria.feedback,
                'recommendation': default_criteria.recommendation,
                'is_exception': False,                    
                'correct_answers': correct,
                'total_questions': total_q,
                'debug_info': debug_info
            }
        
        return {
            'literacy_level': 1,
            'feedback': '기준 데이터가 없습니다.',
            'recommendation': '관리자에게 문의하세요.',
            'is_exception': False,
            'correct_answers': correct,
            'total_questions': total_q,
            'debug_info': debug_info
        }