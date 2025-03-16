import random
from typing import Generator


class ProxyManager:
    def __init__(self, filename: str) -> None:
        self.proxies = self._read_and_format_proxy(filename)
        self._proxy_generator = self._get_proxy()

    def get_formatted_random_proxy(self) -> dict[str, str]:
        """
        Returns formatted proxy in dict format for requests session use
        """
        return random.choice(self.proxies)

    def get_proxy(self) -> dict[str, str]:
        """
        Get the next proxy from the list of proxies
        """
        return next(self._proxy_generator)

    def _read_and_format_proxy(self, filename: str) -> list[dict[str, str]]:
        proxies = self._read_proxies_from_file(filename)
        formatted_proxies = [self._format_proxy(proxy) for proxy in proxies if proxy]
        proxies_dict_format = [self._create_proxy_dict(proxy) for proxy in formatted_proxies]
        return proxies_dict_format

    def _read_proxies_from_file(self, filename: str) -> list[str]:
        with open(filename, "r", encoding="utf-8") as f:
            proxies = f.read().splitlines()
        return proxies

    def _format_proxy(self, proxy: str) -> str:
        splitted_proxy = proxy.split(":", 3)
        if len(splitted_proxy) == 2:
            return proxy
        return f"{splitted_proxy[2]}:{splitted_proxy[3]}@{splitted_proxy[0]}:{splitted_proxy[1]}"

    def _create_proxy_dict(self, formatted_proxy: str) -> dict[str, str]:
        return {"http": f"http://{formatted_proxy}", "https": f"http://{formatted_proxy}"}

    def _get_proxy(self) -> Generator[dict[str, str], None]:
        for proxy in self.proxies:
            yield proxy


if __name__ == "__main__":
    proxy_manager = ProxyManager("./proxies/proxies.txt")
    for i in range(5):
        print(proxy_manager.get_proxy())
