# How to define variables in terraform:
# https://www.terraform.io/docs/configuration/variables.html

# Name of the project, replace "XX" for your
# respective group ID
variable "GCP_PROJECT_NAME" {
    default = ""
}

# A list of machine types is found at:
# https://cloud.google.com/compute/docs/machine-types
# prices are defined per region, before choosing an instance
# check the cost at: https://cloud.google.com/compute/pricing#machinetype
# Minimum required is N1 type = "n1-standard-1, 1 vCPU, 3.75 GB RAM"
variable "GCP_MACHINE_TYPES" {
  type    = list(string)
  default = ["n1-standard-1","n1-standard-2","n1-standard-4","n1-standard-8"]
}

# Minimum required
variable "DISK_SIZE" {
    default = "20"
}

variable "GCP_REGION1" {
    default = "europe-west4-a"
}

variable "USER" {
    default = "afonso_carvalho"
}

variable "SSH_KEY" {
    default = "~/.ssh/ansible"
}

variable "JOB_COORDINATOR_NAME" {
    default = "afonso-job-coordinator-new"
}

#variable "NODES_ONION_NAMES" {
#  type    = list(string)
#  default = ["os-amsterdam-1", "os-finland-1"]
#}

#variable "NODES_ONION_NAMES" {
#  type    = list(string)
#  default = ["os-amsterdam-new", 
#            "os-finland-new", 
 #           "os-london-new", 
 #           "os-los-angeles-new", 
 #           "os-singapore-new",
 #           "os-sydney-new",
 #           "os-tokyo-new"]       
#}

variable "NODES_ONION_NAMES" {
  type    = list(string)
  default = [#"os-amsterdam-1-new", 
            #"os-finland-1-new", 
            #"os-finland-2-new", 
            #"os-london-1-new", 
            #"os-london-2-new", 
            #"os-los-angeles-1-new", 
            #"os-los-angeles-2-new",
            #"os-sao-paulo-1-new",
            #"os-sao-paulo-2-new",
            #"os-singapore-1-new",
            #"os-singapore-2-new",
            #"os-sydney-1-new",
            #"os-sydney-2-new",
            #"os-tokyo-1-new",
            #"os-tokyo-2-new"
            "afonso-os-new"
            ]       
}

#variable "NODES_ONION_REGIONS" {
#  type    = list(string)
#  default = ["europe-west4-a", "europe-north1-a"]
#}

#variable "NODES_ONION_REGIONS" {
 # type    = list(string)
#  default = ["europe-west4-a", 
#            "europe-west1-b",
 #           "europe-west2-c",
 #           "us-west2-a",
 #           "asia-southeast1-b",
  #          "australia-southeast1-b",
  #          "asia-northeast1-b"]
#}

variable "NODES_ONION_REGIONS" {
  type    = list(string)
  default = ["europe-west4-a",
            #"europe-west4-a", 
            #"europe-west1-b",
            #"europe-north1-a",
            #"us-west3-a",
            #"europe-west2-c",
            #"europe-west2-c",
            #"us-west2-a",
            #"us-east1-d",
            #"us-west2-a",
            #"us-west3-a",
            #"asia-east1-b",
            #"asia-southeast1-b",
            #"us-east1-d",
            #"asia-east1-b",
            #"us-west3-a",
            #"australia-southeast1-b",
            #"australia-southeast1-b",
            #"asia-northeast1-b", 
            #"us-east1-d",
            #"asia-northeast1-b"
            #"us-east1-d"
            ]
}

#variable "NODES_ONION_IMAGES" {
#  type    = list(string)
#  default = ["os-amsterdam-1", "os-finland-1"]
#}

variable "NODES_ONION_PAGES" {
  type    = list(string)
  default = ["f2fv76wtuwdvbpci_400_4"#, 
            #"ig2ioz6j2vpcmz27nlqmfdrscijqeqnjv6ku3pkpte7pm53gxeal5hqd_700_9",
            #"jeh4ftzegnmcx75poa3dvzime7yyp2ay6vskfhgis6ikkv3fvzim7sad_100_2",
            #"iyh4h3xzh2aeqsta_500_11",
            #"jnwllvrbzw5nrke6_600_19", 
            #"mybox3a6pmcmbibn_100_3",
            #"nz53a6eqr3jchq5g_0_1",
            #"ppcentrend4erspk_100_3",
            #"tdkncoysfcob7zxe_200_5",
            #"wlriogia33mzs2kl_200_6",
            #"zlhbza2hb6y4qdffehjbsfwlkxb7ovsm4ybgxut5htzc6brcow6syoqd_500_19",
            #"34vnln24rlakgbk6gpityvljieayyw7q4bhdbbgs6zp2v5nbh345zgad_100_1",
            #"55niksbd22qqaedkw36qw4cpofmbxdtbwonxam7ov2ga62zqbhgty3yd_0_5",
            #"5kpq325ecpcncl4o2xksvaso5tuydwj2kuqmpgtmu3vzfxkpiwsqpfid_100_3",
            #"ggonionvhfq7brmj_0_2"
            ]
}

variable "NODES_ONION_POPULARITY" {
  type    = list(string)
  default = ["5326"
            #, "1674", "0850", "0526", "0362", 
            #"0267", "0207", "0165", "0136", "0114",
            #"0097", "0084", "0073", "0065", "0058"
            ]
}

variable "NODES_CLIENT_NAMES" {
  type    = list(string)
  default = ["afonso-client-new",
             "afonso-client-new-2",
             "afonso-client-new-3",
             "afonso-client-new-4",
             "afonso-client-new-5",
             "afonso-client-new-6",
             "afonso-client-new-7",
             "afonso-client-new-8",
             "afonso-client-new-9",
             "afonso-client-new-10",
             "afonso-client-new-11",
             "afonso-client-new-12"
            # "client-amsterdam-1-new", 
            # "client-amsterdam-2-new",
            # "client-belgium-1-new",
            # "client-finland-1-new",
            # "client-finland-2-new",
            # "client-frankfurt-1-new",
            # "client-frankfurt-2-new",
            # "client-iowa-1-new",
            # "client-jakarta-1-new",
            # "client-london-1-new",
            #"client-london-2-new",
            #"client-losangels-1-new",
            #"client-montreal-1-new",
            #"client-oregon-1-new",
            #"client-saopaulo-1-new",
            #"client-singapore-1-new",
            #"client-sydney-1-new",
            #"client-tokyo-1-new",
            #"client-warsaw-1-new",
            #"client-zurich-1-new"
            ]
}

#variable "NODES_CLIENT_REGIONS" {
#  type    = list(string)
#  default = ["europe-west4-a", "europe-west4-a"]
#}

#variable "NODES_CLIENT_REGIONS" {
#  type    = list(string)
#  default = ["europe-west3-a", 
#            "europe-west3-a",
#            "europe-west1-b",
#            "europe-north1-a",
#            "europe-north1-a",
#            "europe-west3-a",
#            "europe-west3-a",
#            "us-central1-a",
#            "asia-southeast2-a",
#            "europe-west2-a",
#            "europe-west2-a",
#            "us-west2-a",
#            "northamerica-northeast1-a",
#            "us-west1-a",
#            "southamerica-east1-a",
#            "asia-southeast1-a",
#            "australia-southeast1-a",
 #           #"asia-northeast1-a",
 #           "europe-central2-a",
#            "europe-west6-a"]
#}

variable "NODES_CLIENT_REGIONS" {
  type    = list(string)
  default = ["europe-west1-b",
            "northamerica-northeast2-a",
            "northamerica-northeast2-a",
            "us-central1-a",
            "asia-southeast2-a",
            "us-central1-a",
            "us-central1-a",
            "europe-west4-a",
            "us-west4-c",
            "us-west4-c",
            # "europe-west3-a", 
            # "europe-west3-a",
            # "europe-west1-b",
            # "northamerica-northeast2-a",
            # "northamerica-northeast2-a",
            # "europe-west3-a",
            # "europe-west3-a",
            #"us-central1-a",
            #"us-west2-a",
            #"us-west4-c",
            #"northamerica-northeast1-a",
            #"us-west4-c",
            #"us-west1-a",
            #"asia-southeast1-a",
            #"us-west4-c",
            #"australia-southeast1-a",
            #"asia-northeast1-a",
            #"us-west4-c",
            #"europe-central2-a",
            #"europe-west6-a"
            ]
}

#variable "NODES_CLIENT_IMAGES" {
#  type    = list(string)
#  default = ["client-amsterdam-1", "client-amsterdam-2"]
#}

#======================= AFONSO: PROBES =====================

variable "NODES_PROBES_NAME" {
  type = list(string)
  default = ["afonso-probe-new",
             "afonso-probe-new-2",
             "afonso-probe-new-3",
             "afonso-probe-new-4",
             "afonso-probe-new-5",
             "afonso-probe-new-6",
             "afonso-probe-new-7",
             "afonso-probe-new-8",
             "afonso-probe-new-9",
             "afonso-probe-new-10",
             "afonso-probe-new-11",
             "afonso-probe-new-12"
             ]
}

variable "NODES_PROBES_REGION" {
  type = list(string)
  default = ["europe-west6-a",
            "europe-west1-b",
            "northamerica-northeast2-a",
            "northamerica-northeast2-a",
            "us-central1-a",
            "asia-southeast2-a",
            "us-central1-a",
            "europe-west1-b",
            "us-central1-a",
            "europe-west4-a",
            # "europe-west3-a",
            # "europe-north1-a",
            "europe-north1-a",
            # "europe-west3-a",
            # "europe-west3-a",
            # "europe-west2-a",
            # "europe-west2-a",
            # "northamerica-northeast1-a",
            "us-west1-a"
            # "southamerica-east1-a",
            # "asia-southeast1-a",
            # "australia-southeast1-a",
            # "asia-northeast1-a",
            # "europe-central2-a",
            ]
}