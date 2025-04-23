import json
import yaml

# 读取JSON文件
with open('exampleSite/data/output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Available keys in data:", list(data.keys()))

# 定义图标映射
icon_mapping = {
    'navigation': 'fa-compass',
    'news': 'fa-newspaper-o',
    'trends': 'fa-line-chart',
    'Qrcode': 'fa-qrcode',
    'movie': 'fa-film',
    'english': 'fa-language',
    'hack': 'fa-code',
    'typing': 'fa-keyboard-o',
    'airPort': 'fa-plane',
    'mirror': 'fa-cloud-download',
    'H5': 'fa-html5',
    'photography': 'fa-camera',
    'music&sound': 'fa-music',
    'stock': 'fa-area-chart',
    'wallpaper': 'fa-picture-o',
    'icon-font': 'fa-flag',
    'productManager': 'fa-product-hunt',
    'ppt': 'fa-file-powerpoint-o',
    'color': 'fa-paint-brush',
    'games': 'fa-gamepad',
    'sites': 'fa-sitemap',
    'art': 'fa-paint-brush',
    'law': 'fa-gavel',
    'ai': 'fa-robot',
    'software': 'fa-desktop'
}

# 定义分类名称映射
category_mapping = {
    'navigation': '导航',
    'news': '新闻资讯',
    'trends': '趋势动态',
    'Qrcode': '二维码',
    'movie': '影视资源',
    'english': '英语学习',
    'hack': '编程开发',
    'typing': '打字输入',
    'airPort': '机场梯子',
    'mirror': '镜像下载',
    'H5': 'H5开发',
    'photography': '摄影图像',
    'music&sound': '音乐音效',
    'stock': '股票基金',
    'wallpaper': '壁纸图片',
    'icon-font': '图标字体',
    'productManager': '产品经理',
    'ppt': 'PPT资源',
    'color': '配色方案',
    'games': '游戏娱乐',
    'sites': '网站导航',
    'art': '艺术设计',
    'law': '法律资源',
    'ai': '人工智能',
    'software': '软件工具'
}

# 转换格式
converted_data = []

# 处理所有类别
for key, value in data.items():
    print(f"\nProcessing category: {key}")
    print(f"Type of value: {type(value)}")
    if isinstance(value, list):
        print(f"Number of items in list: {len(value)}")
        if value:
            print(f"Sample item: {value[0]}")
            
        category_data = {
            'taxonomy': category_mapping.get(key, key),
            'icon': icon_mapping.get(key, 'fa-star'),
            'links': []
        }
        
        for item in value:
            site_data = {}
            
            # 添加必需字段
            if 'title' in item:
                site_data['title'] = item['title']
            if 'url' in item:
                site_data['url'] = item['url']
            if 'description' in item:
                site_data['description'] = item['description']
            if 'logo' in item:
                site_data['logo'] = item['logo']
            if 'qrcode' in item:
                site_data['qrcode'] = item['qrcode']
                
            # 只要有title就添加这个链接
            if 'title' in site_data:
                category_data['links'].append(site_data)
        
        if category_data['links']:  # 只添加非空的类别
            converted_data.append(category_data)
            print(f"Added category {key} with {len(category_data['links'])} links")

print(f"\nTotal categories converted: {len(converted_data)}")

# 写入YAML文件
with open('exampleSite/data/webstack2.yml', 'w', encoding='utf-8') as f:
    yaml.dump(converted_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False) 