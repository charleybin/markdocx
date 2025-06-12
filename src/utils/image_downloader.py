import io
import ssl
import os
import platform
from urllib.request import urlopen, Request
from urllib.parse import urlparse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 抑制SSL警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ImageDownloader:
    """增强的图片下载器，支持SSL验证、Cookie、自定义Headers等"""
    
    def __init__(self, use_browser_cookies=True, verify_ssl=False, custom_headers=None):
        """
        初始化图片下载器
        
        Args:
            use_browser_cookies (bool): 是否使用浏览器Cookie
            verify_ssl (bool): 是否验证SSL证书
            custom_headers (dict): 自定义请求头
        """
        self.use_browser_cookies = use_browser_cookies
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        
        # 设置默认User-Agent
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        if custom_headers:
            default_headers.update(custom_headers)
            
        self.session.headers.update(default_headers)
        
        # 加载浏览器Cookie
        if use_browser_cookies:
            self._load_browser_cookies()
    
    def _load_browser_cookies(self):
        """加载浏览器Cookie"""
        try:
            import browser_cookie3
            
            # 尝试从不同浏览器加载cookie
            browsers = []
            
            try:
                # Chrome cookies
                chrome_cookies = browser_cookie3.chrome()
                browsers.append(('Chrome', chrome_cookies))
            except:
                pass
                
            try:
                # Firefox cookies
                firefox_cookies = browser_cookie3.firefox()
                browsers.append(('Firefox', firefox_cookies))
            except:
                pass
                
            try:
                # Edge cookies
                edge_cookies = browser_cookie3.edge()
                browsers.append(('Edge', edge_cookies))
            except:
                pass
            
            # 使用第一个可用的浏览器cookies
            for browser_name, cookies in browsers:
                if cookies:
                    self.session.cookies.update(cookies)
                    print(f"[COOKIES] Loaded cookies from {browser_name}")
                    break
                    
        except ImportError:
            print("[COOKIES] browser-cookie3 not available, skipping browser cookies")
        except Exception as e:
            print(f"[COOKIES] Failed to load browser cookies: {e}")
    
    def download_image(self, url, timeout=10):
        """
        下载图片
        
        Args:
            url (str): 图片URL
            timeout (int): 超时时间（秒）
            
        Returns:
            io.BytesIO: 图片数据流，失败时返回None
        """
        print(f"[IMAGE] fetching: {url}")
        
        try:
            # 使用requests下载
            response = self.session.get(
                url, 
                timeout=timeout, 
                verify=self.verify_ssl,
                stream=True
            )
            response.raise_for_status()
            
            # 检查内容类型
            content_type = response.headers.get('content-type', '').lower()
            if not any(img_type in content_type for img_type in ['image/', 'application/octet-stream']):
                print(f"[WARNING] Unexpected content type: {content_type}")
            
            # 创建数据流
            image_data = io.BytesIO(response.content)
            print(f"[SUCCESS] Downloaded {len(response.content)} bytes")
            return image_data
            
        except requests.exceptions.SSLError as e:
            print(f"[SSL ERROR] {e}")
            if self.verify_ssl:
                print("[INFO] Retrying with SSL verification disabled...")
                return self._download_with_fallback(url, timeout)
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"[NETWORK ERROR] {e}")
            # 尝试使用urllib作为后备
            return self._download_with_fallback(url, timeout)
            
        except Exception as e:
            print(f"[DOWNLOAD ERROR] {e}")
            return None
    
    def _download_with_fallback(self, url, timeout):
        """使用urllib作为后备下载方法"""
        try:
            print("[FALLBACK] Using urllib with SSL verification disabled")
            
            # 创建SSL上下文，跳过证书验证
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # 创建请求
            req = Request(url)
            req.add_header('User-Agent', self.session.headers['User-Agent'])
            
            # 添加Cookie（如果有的话）
            cookie_header = '; '.join([f"{cookie.name}={cookie.value}" for cookie in self.session.cookies])
            if cookie_header:
                req.add_header('Cookie', cookie_header)
            
            # 下载
            with urlopen(req, timeout=timeout, context=ssl_context) as response:
                image_data = io.BytesIO(response.read())
                print(f"[SUCCESS] Downloaded via fallback")
                return image_data
                
        except Exception as e:
            print(f"[FALLBACK ERROR] {e}")
            return None


# 创建全局下载器实例
_downloader = None

def get_image_downloader(config=None):
    """获取图片下载器实例"""
    global _downloader
    if _downloader is None:
        if config is None:
            config = {
                'use_browser_cookies': True,
                'verify_ssl': False,  # 默认不验证SSL，避免自签名证书问题
                'custom_headers': None
            }
        _downloader = ImageDownloader(**config)
    return _downloader

def download_image(url, timeout=10, config=None):
    """便捷的图片下载函数"""
    downloader = get_image_downloader(config)
    return downloader.download_image(url, timeout) 