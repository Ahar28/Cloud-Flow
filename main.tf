    provider "google" {
    project = "cloud-402400"
    region  = "us-east1-b"
    }

    resource "google_container_cluster" "gke_cluster" {
    name               = "cluster-submission"
    location           = "us-east1-b"
    initial_node_count = 1

     #Disable deletion protection for the cluster
    deletion_protection = false
    
    node_config {
        oauth_scopes = [
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring",
        ]

        disk_size_gb  = 10
        disk_type     = "pd-standard"
        machine_type  = "e2-medium"
        image_type    = "COS_CONTAINERD"
        preemptible   = false

        metadata = {
        disable-legacy-endpoints = "true"
        }
    }
    }

    resource "google_compute_disk" "persistent_volume" {
    name  = "aharnishpv"
    size  = 10
    type  = "pd-standard"
    zone  = "us-east1-b"  # Provide a valid zone value

    labels = {
        environment = "production"
    }
    }

    resource "google_container_node_pool" "node_pool" {
    name       = "default-node-pool"
    cluster    = google_container_cluster.gke_cluster.name
    node_count = 1
    location   = google_container_cluster.gke_cluster.location

    node_config {
        machine_type = "e2-medium"
        disk_size_gb = 10
    }
    }
