import tkinter as tk
from tkinter import messagebox, scrolledtext

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# URLs:
# https://www.google.com/

# https://www.gogole.com/

# https://www.google.com/search?q=hashing&oq=hashing&gs_lcrp=EgZjaHJvbWUqDggAEEUYJxg7GIAEGIoFMg4IABBFGCcYOxiABBiKBTIHCAEQABiABDIHCAIQABiABDIHCAMQABiABDIKCAQQABixAxiABDIHCAUQABiABDIHCAYQABiABDIGCAcQRRg90gEIMTEwMWowajeoAgCwAgA&sourceid=chrome&ie=UTF-8

# https://www.google.com/search?q=data+structures+and+algorithms&oq=data&gs_lcrp=EgZjaHJvbWUqEAgCEAAYkQIYsQMYgAQYigUyBggAEEUYOTIQCAEQABiRAhixAxiABBiKBTIQCAIQABiRAhixAxiABBiKBTIMCAMQABhDGIAEGIoFMgwIBBAAGEMYgAQYigUyCggFEAAYsQMYgAQyDAgGEAAYQxiABBiKBTIGCAcQRRg90gEIMjI0MmowajmoAgawAgHxBe4bHPz-vid1&sourceid=chrome&ie=UTF-8

class URLShortener:
    def __init__(self, initial_size=5):
        self.size = initial_size
        self.table = [[] for _ in range(self.size)]  
        self.count = 0

    def simple_hash(self, url):
        total = 0
        for i, c in enumerate(url):
            total += (i + 1) * ord(c)  
        total = total % (62 ** 6)  
        short_key = ""
        while total>0:
            short_key = chars[total % 62] + short_key
            total //= 62
        return short_key or "a"


    def get_index(self, key):
        return sum(ord(c) for c in key) % self.size

    def load_factor(self):
        return self.count / self.size

    def shorten_url(self, original_url):
        key = self.simple_hash(original_url)
        index = self.get_index(key)
        chain = self.table[index]

        for k, u in chain:
            if u == original_url:
                return f"http://short.ly/{k}"

        chain.append((key, original_url))
        self.count += 1

        if self.load_factor() > 0.7:
            self.rehash()

        return f"http://short.ly/{key}"

    def expand_url(self, short_url):
        key = short_url.split("/")[-1]
        index = self.get_index(key)
        chain = self.table[index]

        found_urls = [u for k, u in chain if k == key]
        if not found_urls:
            return "URL not found!"
        else:
            result = f"Found at index {index} (key={key}):\n"
            for u in found_urls:
                result += f"  {u}\n"
            return result.strip()

    def delete_url(self, short_url):
        key = short_url.split("/")[-1]
        index = self.get_index(key)
        chain = self.table[index]

        for i, (k, u) in enumerate(chain):
            if k == key:
                del chain[i]
                self.count -= 1
                return f"Deleted entry with key {key} at index {index}"
        return "Key not found, deletion failed!"
    
    def display(self):
        output = "\n" + "="*100 + "\n"
        output += f"{'Index':<10}{'Hash Key':<15}{'URLs'}\n"
        output += "="*100 + "\n"

        for i in range(self.size):
            bucket = self.table[i]
            if not bucket:
                output += f"{i:<10}{'---':<15}{'---'}\n"
                continue

            sameKey = {}
            for k, u in bucket:
                sameKey.setdefault(k, []).append(u)

            first_key_printed = False
            for key, urls in sameKey.items():
                for idx, url in enumerate(urls):
                    display_url = (url[:60] + "...") if len(url) > 60 else url

                    if not first_key_printed:
                        if idx == 0:
                            output += f"{i:<10}{key:<15}{display_url}\n"
                            first_key_printed = True
                        else:
                            output += f"{'':<25}{display_url}\n"
                    else:
                        if idx == 0:
                            output += f"{'':<10}{key:<15}{display_url}\n"
                        else:
                            output += f"{'':<25}{display_url}\n"

        output += "="*100 + "\n"
        output += f"Current Load Factor: {self.load_factor():.2f}\n"
        output += "="*100 + "\n"
        return output

    def rehash(self):
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        for chain in old_table:
            for (key, url) in chain:
                self.shorten_url(url)


# ------------------ GUI PART ------------------
class URLShortenerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("URL Shortener (Hashing with Separate Chaining)")
        self.root.geometry("950x600")
        self.root.config(bg="#f9fafc")
        self.shortener = URLShortener()

        tk.Label(
            root,
            text="URL Shortener Using Hashing (Separate Chaining)",
            font=("Segoe UI", 18, "bold"),
            fg="#2c3e50",
            bg="#f9fafc"
        ).pack(pady=15)

        input_frame = tk.Frame(root, bg="#f9fafc")
        input_frame.pack(pady=5)

        tk.Label(
            input_frame,
            text="Enter URL or Short URL:",
            font=("Segoe UI", 11),
            bg="#f9fafc",
            fg="#34495e"
        ).grid(row=0, column=0, padx=5)

        self.input_entry = tk.Entry(
            input_frame,
            width=80,
            font=("Consolas", 10),
            relief="solid",
            bd=1
        )
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(root, bg="#f9fafc")
        btn_frame.pack(pady=10)
        button_style = {"font": ("Segoe UI", 10, "bold"), "width": 15, "bd": 0, "fg": "white", "cursor": "hand2"}

        tk.Button(btn_frame, text="Shorten URL", bg="#2980b9", command=self.shorten_url, **button_style).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Expand URL", bg="#27ae60", command=self.expand_url, **button_style).grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="Delete URL", bg="#e67e22", command=self.delete_url, **button_style).grid(row=0, column=2, padx=6)
        tk.Button(btn_frame, text="Display Table", bg="#8e44ad", command=self.display_table, **button_style).grid(row=0, column=3, padx=6)

        self.output_box = scrolledtext.ScrolledText(
            root,
            width=120,
            height=60,
            wrap=tk.WORD,
            font=("Consolas", 10),
            relief="solid",
            bd=1,
            bg="#fdfdfd"
        )
        self.output_box.pack(pady=10)

    def shorten_url(self):
        url = self.input_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a valid URL.")
            return
        short = self.shortener.shorten_url(url)
        self.output_box.insert(tk.END, f"Shortened URL: {short}\n")
        self.output_box.insert(tk.END, "-"*85 + "\n")
        self.input_entry.delete(0, tk.END)

    def expand_url(self):
        short = self.input_entry.get().strip()
        if not short:
            messagebox.showwarning("Warning", "Please enter the short URL.")
            return
        result = self.shortener.expand_url(short)
        self.output_box.insert(tk.END, result + "\n")
        self.output_box.insert(tk.END, "-"*85 + "\n")
        self.input_entry.delete(0, tk.END)

    def delete_url(self):
        short = self.input_entry.get().strip()
        if not short:
            messagebox.showwarning("Warning", "Please enter the short URL to delete.")
            return
        result = self.shortener.delete_url(short)
        self.output_box.insert(tk.END, result + "\n")
        self.output_box.insert(tk.END, "-"*85 + "\n")
        self.input_entry.delete(0, tk.END)

    def display_table(self):
        output = self.shortener.display()
        self.output_box.insert(tk.END, output + "\n")
        self.output_box.insert(tk.END, "-"*85 + "\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = URLShortenerGUI(root)
    root.mainloop()
