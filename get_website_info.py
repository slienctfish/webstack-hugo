import os
import re
import time
import yaml
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import hashlib

# 创建保存logo的目录
LOGO_DIR = 'static/assets/images/logos/'
os.makedirs(LOGO_DIR, exist_ok=True)

# 加载yaml文件
def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# 保存yaml文件
def save_yaml(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

# 获取网站favicon和元数据
def get_website_info(url):
    try:
        # 确保URL格式正确
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取网站描述
        description = ''
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            description = meta_desc.get('content')
        
        # 如果没有描述，尝试获取OG描述
        if not description:
            og_desc = soup.find('meta', property='og:description')
            if og_desc and og_desc.get('content'):
                description = og_desc.get('content')
        
        # 尝试获取favicon
        icon_url = None
        
        # 方法1：查找link标签中的icon
        for link in soup.find_all('link'):
            rel = link.get('rel', [])
            if isinstance(rel, list):
                rel = ' '.join(rel)
            
            if 'icon' in rel.lower() or 'shortcut icon' in rel.lower():
                icon_path = link.get('href')
                if icon_path:
                    icon_url = urljoin(url, icon_path)
                    break
        
        # 方法2：尝试默认favicon.ico位置
        if not icon_url:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            icon_url = f"{base_url}/favicon.ico"
        
        # 生成文件名
        domain = urlparse(url).netloc
        safe_filename = re.sub(r'[^\w\-_]', '_', domain) + '.png'
        logo_path = os.path.join(LOGO_DIR, safe_filename)
        
        # 下载favicon
        try:
            icon_response = requests.get(icon_url, headers=headers, timeout=5)
            icon_response.raise_for_status()
            
            # 保存favicon
            with open(logo_path, 'wb') as f:
                f.write(icon_response.content)
            
            return {
                'description': description[:100],  # 限制描述长度
                'logo': f'assets/images/logos/{safe_filename}'
            }
        except Exception as icon_error:
            print(f"获取图标失败 {url}: {icon_error}")
            return {
                'description': description[:100],  # 限制描述长度
                'logo': 'assets/images/logos/default.png'  # 使用默认图标
            }
            
    except Exception as e:
        print(f"处理网站失败 {url}: {e}")
        return {
            'description': '',
            'logo': 'assets/images/logos/default.png'  # 使用默认图标
        }

# 主函数
def main():
    yaml_file = 'exampleSite/data/webstack.yml'
    data = load_yaml(yaml_file)
    
    # 创建默认图标
    if not os.path.exists(os.path.join(LOGO_DIR, 'default.png')):
        with open(os.path.join(LOGO_DIR, 'default.png'), 'wb') as f:
            default_icon_url = 'https://www.google.com/favicon.ico'
            try:
                response = requests.get(default_icon_url)
                f.write(response.content)
            except:
                # 创建一个简单的空图标文件
                f.write(b'')
    
    total_sites = sum(len(category['links']) for category in data)
    processed = 0
    
    print(f"开始处理 {total_sites} 个网站...")
    
    for category in data:
        for link in category['links']:
            if 'url' in link:
                processed += 1
                print(f"处理 {processed}/{total_sites}: {link['title']} - {link['url']}")
                
                # 如果已经有logo和description，跳过
                if 'logo' in link and 'description' in link and link['logo'] and link['description']:
                    print(f"  已存在信息，跳过")
                    continue
                
                # 获取网站信息
                info = get_website_info(link['url'])
                
                # 更新link信息
                if 'description' not in link or not link['description']:
                    link['description'] = info['description']
                
                if 'logo' not in link or not link['logo']:
                    link['logo'] = info['logo']
                
                # 每处理10个网站保存一次，防止中断丢失数据
                if processed % 10 == 0:
                    save_yaml(data, yaml_file)
                    print(f"已保存进度 {processed}/{total_sites}")
                
                # 添加延迟，避免请求过快
                time.sleep(1)
    
    # 最终保存
    save_yaml(data, yaml_file)
    print(f"完成! 已处理 {processed} 个网站")

if __name__ == "__main__":
    main() 