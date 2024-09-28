
import time
import argparse
import random
import tracemalloc

# 性能分析装饰器
def performance_analysis(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()  # 开始内存分析
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        _, peak_memory = tracemalloc.get_traced_memory()  # 获取内存峰值
        print(f"函数 {func.__name__} 的执行时间为: {execution_time} 秒")
        print(f"函数 {func.__name__} 的内存峰值为: {peak_memory / 1024 / 1024} MB")
        tracemalloc.stop()  # 停止内存分析
        return result
    return wrapper

# 解析命令行参数
@performance_analysis
# 解析命令行参数
def parse_arguments():
    parser = argparse.ArgumentParser(description='四则运算题目生成器')
    parser.add_argument('-n', type=int, help='生成题目的数量')
    parser.add_argument('-r', type=int, help='数值范围')
    parser.add_argument('-e', help='题目文件的路径')
    parser.add_argument('-a', help='答案文件的路径')
    return parser.parse_args()

# 生成随机的四则运算表达式
def generate_expression(range_limit):
    operators = ['+', '-', '*', '/']
    num_operators = random.randint(1, 3)
    expression = ''
    for _ in range(num_operators):
        operator = random.choice(operators)
        if operator == '/':
            # 生成真分数
            numerator = random.randint(1, range_limit)
            denominator = random.randint(numerator, range_limit)
            expression += f'{numerator}/{denominator} {operator} '
        else:
            # 生成自然数
            operand = random.randint(1, range_limit)
            expression += f'{operand} {operator} '
    operand = random.randint(1, range_limit)
    expression += str(operand)
    return expression

# 计算表达式的答案
def calculate_answer(expression):
    return eval(expression)

# 生成题目和答案
@performance_analysis
def generate_exercises_and_answers(num_exercises, range_limit):
    exercises = []
    answers = []
    while len(exercises) < num_exercises:
        expression = generate_expression(range_limit)
        answer = calculate_answer(expression)
        # 确保结果非负且为整数
        if answer >= 0 and isinstance(answer, int):
            exercises.append(expression)
            answers.append(answer)
    return exercises, answers

# 保存题目和答案到文件
@performance_analysis
def save_exercises_and_answers(exercises, answers):
    with open('Exercises.txt', 'w') as f_exercises, open('Answers.txt', 'w') as f_answers:
        for exercise, answer in zip(exercises, answers):
            f_exercises.write(f"{exercise}\n")
            f_answers.write(f"{answer}\n")

# 评判题目和答案
@performance_analysis
def evaluate_exercises_answers(exercises_file, answers_file):
    student_answers = []
    with open(exercises_file, 'r') as f_exercises, open(answers_file, 'r') as f_answers:
        for exercise, answer in zip(f_exercises, f_answers):
            student_answer = int(input(f"{exercise.strip()} = "))
            student_answers.append((exercise.strip(), int(answer.strip()), student_answer))

    # 统计得分
    correct_count = sum(1 for _, expected, student in student_answers if expected == student)
    wrong_count = sum(1 for _, expected, student in student_answers if expected != student)

    with open('Grade.txt', 'w') as f_grade:
        f_grade.write(f"Correct: {correct_count} ({', '.join(str(i+1) for i, (_, expected, student) in enumerate(student_answers) if expected == student)})\n")
        f_grade.write(f"Wrong: {wrong_count} ({', '.join(str(i+1) for i, (_, expected, student) in enumerate(student_answers) if expected != student)})\n")


if __name__ == '__main__':
    args = parse_arguments()

    if args.n and args.r:
        exercises, answers = generate_exercises_and_answers(args.n, args.r)
        save_exercises_and_answers(exercises, answers)
    elif args.e and args.a:
        evaluate_exercises_answers(args.e, args.a)
    else:
        print('请提供正确的命令行参数')