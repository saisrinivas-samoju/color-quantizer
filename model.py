import matplotlib.image as mpimg
from sklearn.cluster import KMeans
# from app import image, k

# User input
# image = 'flowers.jpg'
# k = 6
############

def process_image(image, k, output_file_path):\
    # Converting image to a numpy array
    img_arr = mpimg.imread(image)
    print("Image loaded and converted to numpy array successfully.")

    # If the image is color image
    if len(img_arr.shape) == 3:
        print("The uploaded image is a color image.")
        (h, w, c) = img_arr.shape
        print(f"The size of the image is {h}px x {w}px")
        # Converting 3D array to 2D array
        img_2darr = img_arr.reshape(h*w, c)
        print("Image has been converted to a 2D array successfully")
    else:  # If the image is in grayscale
        print("The uploaded image is in grayscale.")
        h, w = img_arr.shape
        print(f"The size of the image is {h}px x {w}px")
        c = 1
        img_2darr = img_arr.reshape(h*w, c)
        print("Image has been converted to a 2D array successfully")

    print("Creating the clustering model...")
    model = KMeans(n_clusters=k)
    print("Clustering model created successfully.")

    print("Training the clustering model...")
    clusters = model.fit_predict(img_2darr)
    print("Clustering model trained successfully.")

    # Extract the color codes of the cluster centers

    print("Extracting the cluster centers for reassignment.")
    codes = model.cluster_centers_.round().astype("uint8")
    print("Cluster centers extracted successfully.")

    # Reproducing the cluster centers in the same position as img_2darr samples
    print("Creating the quantized image")
    if c == 1:
        quantized_image = codes[clusters].reshape(h, w)
    else:
        quantized_image = codes[clusters].reshape(h, w, c)
    print("Successfully created the quantized image")

    # Saving the quantized image
    print("Saving the quantized image")
    mpimg.imsave(fname=output_file_path, arr=quantized_image)
    print("Successfully saved the quantized image.")
