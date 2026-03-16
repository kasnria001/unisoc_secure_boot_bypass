import sys  
import os  
  
def modify_binary_file(file_path):  
      
    if not os.path.isfile(file_path):  
        print(f"错误：文件 {file_path} 不存在")  
        return False  
  
    try:  
          
        with open(file_path, 'rb') as f:  
            data = bytearray(f.read())  
  
          
        target_bytes = bytes.fromhex('77 32 40 B9')  
        new_bytes = bytes.fromhex('77 3A 40 B9')  
        follow_bytes = bytes.fromhex('35 00 80 52 F7 02 08 91 51 00 00 14')  
  
          
        target_index = data.find(target_bytes)  
        if target_index == -1:  
            print(f"未找到目标字节序列 {target_bytes.hex()}")  
            return False  
  
          
        data[target_index:target_index+len(target_bytes)] = new_bytes  
  
          
        start_index = target_index + len(new_bytes)  
        if start_index + len(follow_bytes) > len(data):  
            print("文件长度不足，无法完成修改")  
            return False  
  
          
        data[start_index:start_index+len(follow_bytes)] = follow_bytes  
  
          
        with open(file_path, 'wb') as f:  
            f.write(data)  
        print(f"文件修改成功，修改位置：{target_index}")  
        return True  
  
    except PermissionError:  
        print(f"错误：没有权限修改文件 {file_path}")  
    except Exception as e:  
        print(f"处理过程中发生错误: {str(e)}")  
    return False  
  
if __name__ == '__main__':  
      
    file_path = input("请输入要修改的二进制文件完整路径(UBOOT/LK FILE): ")  
      
      
    if not file_path.strip():  
        print("错误：文件路径不能为空")  
    else:  
        modify_binary_file(file_path)
