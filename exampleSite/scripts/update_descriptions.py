import yaml
import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urlparse

# 加载YAML文件
def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# 保存YAML文件
def save_yaml(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

# 从网站获取标题
def get_website_title(url):
    try:
        # 确保URL格式正确
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        
        # 尝试检测并设置正确的编码
        if response.encoding.lower() == 'iso-8859-1':
            # 尝试从网页内容中获取编码
            encodings = re.findall(r'charset=["\']?([\w-]+)', response.text)
            if encodings:
                response.encoding = encodings[0]
            else:
                response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取网站标题的方法
        title = ""
        
        # 方法1：从title标签获取
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        
        # 方法2：从og:title元标签获取
        if not title:
            og_title = soup.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                title = og_title.get('content').strip()
        
        # 方法3：从twitter:title元标签获取
        if not title:
            twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
            if twitter_title and twitter_title.get('content'):
                title = twitter_title.get('content').strip()
        
        # 如果还是没有找到标题，使用域名作为标题
        if not title:
            domain = urlparse(url).netloc
            if domain.startswith('www.'):
                domain = domain[4:]
            title = domain
        
        return title
        
    except Exception as e:
        print(f"处理网站失败 {url}: {e}")
        # 返回URL的域名作为标题
        domain = urlparse(url).netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain

# 主函数
def main():
    yaml_file = 'exampleSite/data/webstack.yml'
    data = load_yaml(yaml_file)
    
    total_sites = sum(len(category['links']) for category in data)
    processed = 0
    
    print(f"开始处理 {total_sites} 个网站...")
    
    for category in data:
        for link in category['links']:
            if 'url' in link:
                processed += 1
                print(f"处理 {processed}/{total_sites}: {link['title']} - {link['url']}")
                
                # 获取网站标题
                title = get_website_title(link['url'])
                
                # 更新link信息
                link['description'] = title
                
                # 每处理10个网站保存一次，防止中断丢失数据
                if processed % 10 == 0:
                    save_yaml(data, yaml_file)
                    print(f"已保存进度 {processed}/{total_sites}")
                
                # 添加延迟，避免请求过快
                time.sleep(1)
    
    # 最终保存
    save_yaml(data, yaml_file)
    print(f"完成! 已处理 {processed} 个网站，将description替换为网站标题")

if __name__ == "__main__":
    main() 