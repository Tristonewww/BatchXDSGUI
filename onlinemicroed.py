import sys
import time

def main(input_path):
    print(f"Received input path: {input_path}")

    # 设置循环运行的次数
    num_iterations = 6

    for i in range(num_iterations):
        print(f"Running iteration {i + 1}...")
        time.sleep(1)  # 1秒钟打印一次

    print("Completed all iterations.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No input path provided.")
    else:
        input_path = sys.argv[1]
        main(input_path)
