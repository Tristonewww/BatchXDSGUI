import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python make_clusters.py <input_path> <cluster_distance_value>")
        return
    
    input_path = sys.argv[1]
    cluster_distance_value = sys.argv[2]

    print(f"Received input path: {input_path}")
    print(f"Received cluster distance value: {cluster_distance_value}")

if __name__ == "__main__":
    main()
