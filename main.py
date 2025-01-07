import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
from collections import deque


def is_top_level_domain(url):
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    return not path and parsed.scheme in ['http', 'https']


def get_domain(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def scrape_links_dfs(start_url, max_depth=5):
    stack = [(start_url, 0)]  # (url, depth)
    visited = set()

    while stack and len(visited) < 100:  # Limit to 100 sites for safety
        current_url, depth = stack.pop()

        if depth >= max_depth:
            continue

        if current_url in visited:
            continue

        try:
            response = requests.get(current_url, timeout=5)
            if response.status_code != 200:
                continue

            visited.add(current_url)
            print(f"Visiting [{depth}]: {current_url}")

            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all('a', href=True)

            # Process all links from the page
            for link in links:
                href = link['href']
                full_url = urljoin(current_url, href)

                # Only add if it's a new top-level domain
                if (is_top_level_domain(full_url) and
                        full_url not in visited and
                        get_domain(full_url) not in [get_domain(v) for v in visited]):
                    stack.append((full_url, depth + 1))

        except Exception as e:
            print(f"Error processing {current_url}: {str(e)}")
            continue

    return visited


# Main execution
if __name__ == "__main__":
    start_url = "https://wikipedia.com/"
    visited_sites = scrape_links_dfs(start_url, max_depth=3)
    print("\nVisited sites:")
    for site in visited_sites:
        print(site)
