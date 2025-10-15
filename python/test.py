import subprocess
import os
import re

# 配置信息
BOOKSIM_PATH = "booksim2/src"
# base config
CONFIG_FILE_BASE = "../../config/base" 
OUTPUT_FILE_BASE = "./output/booksim2_results_base.txt"
LOG_FILE_BASE = "./output/booksim2_full_log_base.txt"
INTEGERS_FILE_BASE = "./output/booksim2_integers_base.txt"  # 新增：整数保存文件
# test config
CONFIG_FILE = "../../config/test"
OUTPUT_FILE = "./output/booksim2_results.txt"
LOG_FILE = "./output/booksim2_full_log.txt"
INTEGERS_FILE = "./output/booksim2_integers.txt"  # 新增：整数保存文件

def extract_integers_from_line(line):
    """从单行文本中提取所有整数[1,2](@ref)"""
    # 使用正则表达式提取整数（包括负数）
    integers = re.findall(r'-?\d+', line)
    return [int(num) for num in integers] if integers else []

def run_booksim_base():
    """运行BookSim并提取特定输出行中的整数"""
    
    original_dir = os.getcwd()
    os.chdir(BOOKSIM_PATH) 
    command = ["./booksim", CONFIG_FILE_BASE]

    target_patterns = [
        "Warmed up ...Time used is",
        "Time taken is"
    ]

    try:
        with open(os.path.join(original_dir, LOG_FILE_BASE), 'w') as log_file, \
             open(os.path.join(original_dir, OUTPUT_FILE_BASE), 'w') as result_file, \
             open(os.path.join(original_dir, INTEGERS_FILE_BASE), 'w') as integers_file:  # 新增整数文件
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            target_lines = []
            all_integers = []  # 存储所有提取的整数
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    log_file.write(output)
                    log_file.flush()
                    
                    for pattern in target_patterns:
                        if pattern in output:
                            target_lines.append(output.strip())
                            result_file.write(output)
                            result_file.flush()
                            
                            # 提取整数[1,3](@ref)
                            integers = extract_integers_from_line(output)
                            if integers:
                                all_integers.extend(integers)
                                # 将整数保存到文件
                                integers_file.write(f"目标行: {output.strip()}\n")
                                integers_file.write(f"提取整数: {integers}\n")
                                integers_file.write("-" * 50 + "\n")
                                integers_file.flush()
                                #print(f"找到目标行: {output.strip()} -> 提取整数: {integers}")
            
            print("=" * 50)
            #print(f"完整日志已保存到: {LOG_FILE_BASE}")
            #print(f"目标行已保存到: {OUTPUT_FILE_BASE}")
            #print(f"整数结果已保存到: {INTEGERS_FILE_BASE}")
            #print(f"共找到 {len(target_lines)} 个目标行，提取 {len(all_integers)} 个整数")
            
            return target_lines, all_integers  # 返回目标行和整数列表
        
    except Exception as e:
        print(f"错误: {e}")
        return [], []
    finally:
        os.chdir(original_dir)

def run_booksim():
    """运行BookSim并提取运行周期"""
    
    original_dir = os.getcwd()
    os.chdir(BOOKSIM_PATH) 
    command = ["./booksim", CONFIG_FILE]

    target_patterns = [
        "Warmed up ...Time used is",
        "Time taken is"
    ]

    try:
        with open(os.path.join(original_dir, LOG_FILE), 'w') as log_file, \
             open(os.path.join(original_dir, OUTPUT_FILE), 'w') as result_file, \
             open(os.path.join(original_dir, INTEGERS_FILE), 'w') as integers_file:
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            target_lines = []
            all_integers = []
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    log_file.write(output)
                    log_file.flush()
                    
                    for pattern in target_patterns:
                        if pattern in output:
                            target_lines.append(output.strip())
                            result_file.write(output)
                            result_file.flush()
                            
                            integers = extract_integers_from_line(output)
                            if integers:
                                all_integers.extend(integers)
                                integers_file.write(f"目标行: {output.strip()}\n")
                                integers_file.write(f"提取整数: {integers}\n")
                                integers_file.write("-" * 50 + "\n")
                                integers_file.flush()
                                #print(f"找到目标行: {output.strip()} -> 提取整数: {integers}")
            
            print("=" * 50)
            #print(f"完整日志已保存到: {LOG_FILE}")
            #print(f"目标行已保存到: {OUTPUT_FILE}")
            #print(f"整数结果已保存到: {INTEGERS_FILE}")
            #print(f"共找到 {len(target_lines)} 个目标行，提取 {len(all_integers)} 个整数")
            
            return target_lines, all_integers
        
    except Exception as e:
        print(f"错误: {e}")
        return [], []
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    # 运行base配置
    results_base, integers_base = run_booksim_base()
    
    if results_base:
        print("base配置提取到的目标行:")
        for i, line in enumerate(results_base, 1):
            print(f"{i}: {line}")
    else:
        print("base配置未找到目标行")
    
    print("=" * 50)
    
    # 运行test配置
    results, integers = run_booksim()
    
    if results:
        print("test配置提取到的目标行:")
        for i, line in enumerate(results, 1):
            print(f"{i}: {line}")
    else:
        print("test配置未找到目标行")
    
    print("=" * 50)
    
    # 对比分析两个配置的结果
    if integers_base and integers:
        print("结果：")
        print(f"base配置整数: {integers_base}")
        print(f"test配置整数: {integers}")
        print(f"差值分析: {[test - base for test, base in zip(integers, integers_base)]}")
        print(f"增益分析: {[round(base/test, 2) for test, base in zip(integers, integers_base)]}")
        print(f"增益分析(去除warm clk): {round((integers_base[1]-integers_base[0])/(integers[1]-integers[0]), 2)}")