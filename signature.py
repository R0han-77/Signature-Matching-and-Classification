import cv2
from skimage.metrics import structural_similarity as ssim

def match(path1, path2):
    try:
        # read the images
        img1 = cv2.imread(path1)
        img2 = cv2.imread(path2)
        if img1 is None or img2 is None:
            raise ValueError("One of the images could not be loaded.")

        # turn images to grayscale
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # resize images for comparison
        img1 = cv2.resize(img1, (300, 300))
        img2 = cv2.resize(img2, (300, 300))

        # display both images
        cv2.imshow("Image 1", img1)
        cv2.imshow("Image 2", img2)
        cv2.waitKey(3000)  # display images for 3 seconds
        cv2.destroyAllWindows()

        similarity_value = "{:.2f}".format(ssim(img1, img2) * 100)
        return float(similarity_value)
    except Exception as e:
        print(f"Error during image matching: {e}")
        return 0.0
