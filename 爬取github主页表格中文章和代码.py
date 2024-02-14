# GitHub Pages上的链接地址在页面发布后通常是固定的，除非网页内容被更新并更改了链接。对于嵌入在Markdown表格中的PDF文章和代码链接，你可以编写Python脚本使用requests库来获取网页内容，并利用BeautifulSoup等HTML解析库提取出需要的链接。下面是一个基本的示例脚本，用于爬取指定GitHub Pages页面上Markdown表格中的PDF和代码链接，并下载相关资源：

# ```python
import requests
from bs4 import BeautifulSoup
import os

# GitHub Pages 页面URL
url = "https://example.github.io/repo-name/pages-url"

# 发送GET请求获取页面内容
response = requests.get(url)
response.raise_for_status()

# 解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

# 查找Markdown表格
table = soup.find('table')  # 这里假设表格是唯一的，实际项目中可能需要更精确的选择器

# 遍历表格中的所有链接
for row in table.find_all('tr'):  # 假设每一行都有链接
    for cell in row.find_all(['a', 'td']):  # 根据实际结构选择查找链接的位置
        link = cell.find('a')
        if link and (link.get('href').endswith('.pdf') or '/blob/' in link.get('href')):
            href = link['href']
            
            # 分别处理PDF文件和代码仓库链接
            if href.endswith('.pdf'):
                pdf_url = href  # 如果PDF链接是绝对路径，则可以直接下载
                # 若为相对路径，则需要与base_url拼接
                if not pdf_url.startswith('http'):
                    pdf_url = f'https://github.com/{os.path.dirname(url)}/{pdf_url}'
                
                # 下载PDF文件
                response_pdf = requests.get(pdf_url)
                with open(os.path.basename(pdf_url), 'wb') as f:
                    f.write(response_pdf.content)

            elif '/blob/' in href:  # 处理代码仓库链接
                code_url = href.replace('/blob/', '/')  # 将blob链接转换为raw链接
                code_url += '?raw=true'  # 添加raw参数以直接下载代码文件
                
                # 下载代码文件
                response_code = requests.get(code_url)
                with open(os.path.basename(code_url), 'wb') as f:
                    f.write(response_code.content)

# 注意：上述代码只是一个基础示例，具体实现时需根据实际页面结构进行调整
# ```

# 这个脚本没有考虑访问速率限制、授权问题以及错误处理等情况，请在实际使用时确保遵守GitHub API使用政策，并合理控制抓取速度，以免触犯网站服务条款。

# 另外，如果PDF或代码链接嵌入在Markdown中，但不是直接在表格内（例如通过内联HTML标签插入），则可能需要针对具体的Markdown解析规则进行适配。