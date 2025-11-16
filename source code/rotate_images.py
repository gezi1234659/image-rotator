import os
from PIL import Image
import sys

def get_image_files(folder_path):
    """获取文件夹中的所有图片文件"""
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    try:
        files = os.listdir(folder_path)
        image_files = [f for f in files if os.path.splitext(f)[1].lower() in supported_formats]
        return image_files
    except FileNotFoundError:
        return None
    except PermissionError:
        return None

def batch_rotate_images(input_folder, output_folder, rotation_angle):
    """
    批量旋转文件夹中的所有图片
    
    参数:
    input_folder: 输入图片文件夹路径
    output_folder: 输出文件夹路径
    rotation_angle: 旋转角度(0-360度)
    """
    
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"已创建输出文件夹: {output_folder}")
    
    # 获取图片文件
    image_files = get_image_files(input_folder)
    
    if not image_files:
        print("在输入文件夹中没有找到支持的图片文件!")
        return
    
    processed_count = 0
    error_count = 0
    
    # 处理每个图片文件
    for filename in image_files:
        try:
            # 构建完整的文件路径
            input_path = os.path.join(input_folder, filename)
            
            # 分离文件名和扩展名
            name, ext = os.path.splitext(filename)
            
            # 创建新文件名（添加旋转角度标识）
            new_filename = f"{name}_rotated_{int(rotation_angle)}_degrees{ext}"
            output_path = os.path.join(output_folder, new_filename)
            
            # 打开并旋转图片
            with Image.open(input_path) as img:
                # 旋转图片
                rotated_img = img.rotate(rotation_angle, expand=True)
                
                # 保存旋转后的图片（保持原始格式）
                rotated_img.save(output_path)
                
                print(f"已处理: {filename} -> {new_filename}")
                processed_count += 1
                
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {str(e)}")
            error_count += 1
    
    # 输出处理结果
    print(f"\n处理完成!")
    print(f"成功处理: {processed_count} 个文件")
    print(f"处理失败: {error_count} 个文件")
    # print(f"输出文件夹: {output_folder}")

def get_valid_folder(prompt):
    """获取有效的文件夹路径，并显示找到的图片数量"""
    while True:
        folder_path = input(prompt).strip()
        
        # 如果用户输入为空，使用当前工作目录
        if not folder_path:
            folder_path = os.getcwd()
        
        # 处理相对路径
        if not os.path.isabs(folder_path):
            folder_path = os.path.abspath(folder_path)
        
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # 扫描图片文件并显示数量
            image_files = get_image_files(folder_path)
            if image_files is None:
                print(f"错误: 无法访问文件夹 '{folder_path}'! 请重新输入。")
                continue
            
            print(f"在文件夹中找到 {len(image_files)} 个图片文件")
            return folder_path
        else:
            print(f"错误: 文件夹 '{folder_path}' 不存在! 请重新输入。")

def get_output_folder(input_folder):
    """获取输出文件夹路径"""
    while True:
        print("(直接回车将在输入文件夹下创建out文件夹)")
        output_path = input("请输入输出的文件夹路径: ").strip()
        
        # 如果用户直接回车，使用默认路径（输入文件夹下的out文件夹）
        if not output_path:
            output_path = os.path.join(input_folder, "out")
            print(f"使用默认输出路径: {output_path}")
            return output_path
        
        # 处理相对路径
        if not os.path.isabs(output_path):
            output_path = os.path.join(input_folder, output_path)
        
        # 检查路径是否有效
        try:
            # 如果路径已经存在且是文件而不是文件夹，报错
            if os.path.exists(output_path) and not os.path.isdir(output_path):
                print(f"错误: '{output_path}' 已存在但不是文件夹! 请重新输入。")
                continue
            
            # 路径不存在或存在且是文件夹，直接返回（在转换时自动创建）
            print(f"使用输出路径: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"处理路径时出错: {str(e)}! 请重新输入。")

def main():
    print("=== 图片批量旋转工具 ===\n")
    
    # 获取输入文件夹
    print("请输入包含图片的文件夹路径:")
    print("(直接回车使用当前目录)")
    input_folder = get_valid_folder("输入文件夹路径: ")
    
    # 获取旋转角度
    while True:
        try:
            angle_input = input("请输入旋转角度(0-360度): ").strip()
            rotation_angle = float(angle_input)
            if 0 <= rotation_angle <= 360:
                break
            else:
                print("错误: 角度必须在0-360度之间!")
        except ValueError:
            print("错误: 请输入有效的数字!")
    
    # 获取输出文件夹
    output_folder = get_output_folder(input_folder)
    
    # 再次确认图片数量
    image_files = get_image_files(input_folder)
    
    print(f"\n配置信息:")
    print(f"输入文件夹: {input_folder}")
    print(f"输出文件夹: {output_folder}")
    print(f"旋转角度: {rotation_angle}度")
    print(f"待处理图片: {len(image_files)} 个")
    
    # 确认开始处理
    confirm = input("\n是否开始处理? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', '是']:
        print("操作已取消。")
        return
    
    # 执行批量旋转
    batch_rotate_images(input_folder, output_folder, rotation_angle)
    
    # 等待用户按键退出
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()