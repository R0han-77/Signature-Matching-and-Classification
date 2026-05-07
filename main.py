import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import os
import cv2
from signature import match

# Match Threshold
THRESHOLD = 85

def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp(sign=1):
    try:
        cam = cv2.VideoCapture(0, cv2.CAP_ANY)
        cv2.namedWindow("test")

        while True:
            ret, frame = cam.read()
            if not ret:
                print("Failed to capture image")
                break
            cv2.imshow("test", frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                if not os.path.isdir('temp'):
                    os.mkdir('temp', mode=0o777)  # make sure the directory exists
                img_name = os.path.join('temp', f'test_img{sign}.png')
                cv2.imwrite(filename=img_name, img=frame)
                print(f"{img_name} written!")
        cam.release()
        cv2.destroyAllWindows()
        return True
    except Exception as e:
        print(f"Error during image capture: {e}")
        return False

def captureImage(ent, sign=1):
    try:
        filename = os.path.join(os.getcwd(), 'temp', f'test_img{sign}.png')
        res = messagebox.askquestion(
            'Click', 'Press Space Bar to capture image and ESC to exit')
        if res == 'yes':
            if capture_image_from_cam_into_temp(sign=sign):
                ent.delete(0, tk.END)
                ent.insert(tk.END, filename)
        return True
    except Exception as e:
        print(f"Error during image capture: {e}")
        return False

def checkSimilarity(window, path1, path2):
    try:
        result = match(path1=path1, path2=path2)
        if result <= THRESHOLD:
            messagebox.showerror("Failure: Signatures Do Not Match",
                                 f"Signatures are {result:.2f} % similar!!")
        else:
            messagebox.showinfo("Success: Signatures Match",
                                f"Signatures are {result:.2f} % similar!!")
    except Exception as e:
        print(f"Error during similarity check: {e}")

def main_app():
    root = tk.Tk()
    root.title("Signature Matching")
    root.geometry("500x500")
    root.configure(bg="#194569")

    # Use ttk styles for a more modern look
    style = ttk.Style()
    style.configure("TButton", font=("sans-serif", 12), foreground="black", background="#91aec4", borderwidth=0, relief="flat")
    style.map("TButton", background=[('active', '#91aec4')])
    style.configure("TLabel", font=("sans-serif", 12), background="#194569", foreground="white")
    style.configure("TEntry", font=("sans-serif", 12), foreground="black", background="#ffffff", relief="flat")

    # Center-align the title label
    uname_label = ttk.Label(root, text="Compare Signatures:", font=("sans-serif", 16), background="#194569")
    uname_label.grid(row=0, column=0, columnspan=3, pady=20, padx=10, sticky='nsew')

    # Labels and entries for image paths
    img1_message = ttk.Label(root, text="Input 1", background="#194569")
    img1_message.grid(row=1, column=0, pady=10, padx=10, sticky='e')

    image1_path_entry = ttk.Entry(root, width=40)
    image1_path_entry.grid(row=1, column=1, pady=10, padx=10)

    img1_capture_button = ttk.Button(
        root, text="Capture", command=lambda: captureImage(ent=image1_path_entry, sign=1))
    img1_capture_button.grid(row=1, column=2, pady=10, padx=10)

    img1_browse_button = ttk.Button(
        root, text="Browse", command=lambda: browsefunc(ent=image1_path_entry))
    img1_browse_button.grid(row=2, column=2, pady=10, padx=10)

    img2_message = ttk.Label(root, text="Input 2", background="#194569")
    img2_message.grid(row=3, column=0, pady=10, padx=10, sticky='e')

    image2_path_entry = ttk.Entry(root, width=40)
    image2_path_entry.grid(row=3, column=1, pady=10, padx=10)

    img2_capture_button = ttk.Button(
        root, text="Capture", command=lambda: captureImage(ent=image2_path_entry, sign=2))
    img2_capture_button.grid(row=3, column=2, pady=10, padx=10)

    img2_browse_button = ttk.Button(
        root, text="Browse", command=lambda: browsefunc(ent=image2_path_entry))
    img2_browse_button.grid(row=4, column=2, pady=10, padx=10)

    compare_button = ttk.Button(
        root, text="Compare", command=lambda: checkSimilarity(window=root,
                                                             path1=image1_path_entry.get(),
                                                             path2=image2_path_entry.get(),))
    compare_button.grid(row=5, column=0, columnspan=3, pady=20)

    # Configure grid layout to make it more responsive
    for i in range(3):
        root.grid_columnconfigure(i, weight=1)
    for i in range(6):
        root.grid_rowconfigure(i, weight=1)

    root.mainloop()

def show_splash():
    splash = tk.Tk()
    splash.title("Welcome")
    splash.geometry("500x400")
    splash.configure(bg="#194569")

    # Load and display the GIF
    gif_label = ttk.Label(splash)
    gif_label.pack(expand=True)

    # Path to the GIF file
    gif_path = "loading_main.gif"

    gif = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(frame.convert('RGBA')) for frame in ImageSequence.Iterator(gif)]
    
    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind >= len(frames):
            ind = 0
        gif_label.configure(image=frame)
        splash.after(100, update, ind)
    
    splash.after(0, update, 0)

    # Close splash screen after 3 seconds and start main app
    splash.after(3000, lambda: [splash.destroy(), main_app()])

    splash.mainloop()

if __name__ == "__main__":
    show_splash()
