import customtkinter as ctk
from PIL import Image
from io import BytesIO
import requests

from search_torrent import search_movie
from download import download_torrent, format_downloads, change_download


isResultsPage = True

download_icon = ctk.CTkImage(
    light_image=Image.open("assets/hard-drive-download.png"),
    dark_image=Image.open("assets/hard-drive-download.png"),
    size=(32, 32)
)

cloud_icon = ctk.CTkImage(
    light_image=Image.open("assets/cloud-download.png"),
    dark_image=Image.open("assets/cloud-download.png"),
    size=(22, 22)
)

root = ctk.CTk()
root.title("TorDL")
root.geometry("800x500")


def create_movie_row(results_frame, result):
    movie_frame = ctk.CTkFrame(
        results_frame
    )

    movie_frame.pack(
        fill="x",
        padx=10,
        pady=5
    )

    movie_frame.columnconfigure(1, weight=1)

    if result["poster_url"] == None:

        error_label = ctk.CTkLabel(
            movie_frame,
            text="No\nPoster\navalaible"
        )

        error_label.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=10,
            pady=10
        )

    else:
        response = requests.get(result["poster_url"])
        image = Image.open(BytesIO(response.content))

        poster = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(70, 105)
        )

        poster_label = ctk.CTkLabel(
            movie_frame,
            image=poster,
            text=""
        )


        poster_label.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=10,
            pady=10
        )

    info_frame = ctk.CTkFrame(
        movie_frame,
        fg_color="transparent"
    )

    info_frame.grid(
        row=0,
        column=1,
        sticky="w",
        padx=10
    )

    title_label = ctk.CTkLabel(
        info_frame,
        text=result["movie_title"],
        font=("Arial", 14, "bold")
    )

    title_label.pack(anchor="w")

    torrent_label = ctk.CTkLabel(
        info_frame,
        text=result["torrent_title"],
        font=("Arial", 12),
        text_color="gray"
    )

    torrent_label.pack(anchor="w")

    action_frame = ctk.CTkFrame(
        movie_frame,
        fg_color="transparent"
    )

    action_frame.grid(
        row=0,
        column=2,
        padx=10,
        sticky="e"
    )

    size_label = ctk.CTkLabel(
        action_frame,
        text=result["size"]
    )

    size_label.pack()

    download_button = ctk.CTkButton(
        action_frame,
        text="",
        image=download_icon,
        font=("Arial", 18),
        width=42,
        height=42,
        corner_radius=6,
        command=lambda: start_download(result["magnet"]),
    )

    download_button.pack()


def clear_results():
    for widget in results_frame.winfo_children():
        widget.destroy()


def launch_search():
    global isResultsPage

    if isResultsPage == False:
        show_search_page()
        isResultsPage = True
    else:
        query = search_entry.get()

        results = search_movie(query)


        clear_results()

        for result in results:
            create_movie_row(
                results_frame,
                result
            )



def show_search_page():
    global isResultsPage

    isResultsPage = True

    downloads_page.pack_forget()

    search_page.pack(
        fill="both",
        expand=True
    )


def show_downloads_page():
    global isResultsPage

    isResultsPage = False
    search_page.pack_forget()

    downloads_page.pack(
        fill="both",
        expand=True
    )

    refresh_downloads()



def clear_downloads():
    for widget in downloads_frame.winfo_children():
        widget.destroy()


def create_download_row(parent, download):
    row = ctk.CTkFrame(parent)

    row.pack(
        fill="x",
        padx=10,
        pady=5
    )

    row.columnconfigure(0, weight=1)

    # TITLE
    title_label = ctk.CTkLabel(
        row,
        text=download["title"],
        font=("Arial", 14, "bold")
    )

    title_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=10,
        pady=(10, 0)
    )

    # STATUS
    status_button = ctk.CTkButton(
        row,
        text=download["status"],
        command=lambda: change_download(download["id"],download["status"])
    )

    status_button.grid(
        row=0,
        column=1,
        padx=10,
        pady=(10, 0)
    )

    # PROGRESS BAR
    progress_bar = ctk.CTkProgressBar(row)

    progress_bar.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=10,
        pady=10
    )

    progress_bar.set(
        download["progress"] / 100
    )

    # PROGRESS %
    progress_label = ctk.CTkLabel(
        row,
        text=f'{download["progress"]:.1f}%'
    )

    progress_label.grid(
        row=1,
        column=1,
        padx=10
    )

    # SPEED
    speed_label = ctk.CTkLabel(
        row,
        text=f'{download["speed"] / 1024**2:.1f} MB/s',
        text_color="gray"
    )

    speed_label.grid(
        row=2,
        column=0,
        sticky="w",
        padx=10,
        pady=(0, 10)
    )


def refresh_downloads():
    if isResultsPage:
        return

    downloads = format_downloads()

    clear_downloads()

    for download in downloads:
        create_download_row(
            downloads_frame,
            download
        )

    root.after(
        2000,
        refresh_downloads
    )

def show_toast(message, type="info"):
    toast = ctk.CTkToplevel(root)

    toast.overrideredirect(True)
    toast.attributes("-topmost", True)

    width = 260
    height = 60

    root.update_idletasks()

    x = root.winfo_x() + root.winfo_width() - width - 20
    y = root.winfo_y() + 20

    toast.geometry(f"{width}x{height}+{x}+{y}")

    if type == "success":
        color = "#2E7D32"

    elif type == "error":
        color = "#B3261E"

    else:
        color = "#3A3A3A"
    
    frame = ctk.CTkFrame(
        toast,
        corner_radius=10,
        fg_color=color,
    )

    frame.pack(
        fill="both",
        expand=True
    )

    label = ctk.CTkLabel(
        frame,
        text=message,
        font=("Arial", 13)
    )

    label.pack(
        expand=True,
        padx=15,
        pady=10
    )

    toast.after(
        2500,
        toast.destroy
    )


def start_download(magnet):
    response = download_torrent(magnet)
    if response == True:
        show_toast("Download started", "success")


# =========================
# HEADER
# =========================

header_frame = ctk.CTkFrame(root)

header_frame.pack(
    fill="x",
    padx=10,
    pady=10
)

nas_button = ctk.CTkButton(
        header_frame,
        text="",
        image=cloud_icon,
        font=("Arial", 18),
        width=32,
        height=32,
        corner_radius=6,
        command=show_downloads_page
    )

nas_button.pack(side="left", padx=(0, 5))


search_entry = ctk.CTkEntry(
    header_frame,
    font=("Arial", 16),
)

search_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 5)
)


search_button = ctk.CTkButton(
    header_frame,
    text="Search",
    command=launch_search
)

search_button.pack(
    side="right",
)


# =========================
# RESULTS CONTAINER
# =========================



results_container = ctk.CTkFrame(root)

results_container.pack(
    fill="both",
    expand=True
)

search_page = ctk.CTkFrame(
    results_container,
    fg_color="transparent"
)

search_page.pack(
    fill="both",
    expand=True
)

# =========================
# SCROLLABLE FRAME
# =========================

results_frame = ctk.CTkScrollableFrame(
    search_page
)

results_frame.pack(
    fill="both",
    expand=True
)




downloads_page = ctk.CTkFrame(
    results_container,
    fg_color="transparent"
)

downloads_title = ctk.CTkLabel(
    downloads_page,
    text="Downloads",
    font=("Arial", 22, "bold")
)

downloads_title.pack(
    anchor="w",
    padx=20,
    pady=20
)


downloads_frame = ctk.CTkScrollableFrame(
    downloads_page
)

downloads_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=(0, 10)
)



root.mainloop()