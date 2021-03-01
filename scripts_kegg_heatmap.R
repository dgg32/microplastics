library(tidyverse)
library(stringr)
library(ComplexHeatmap)

setwd("/data/microplastics/data")

genes_pathway_file <- read_delim("kegg/genes_pathway.list",
                                 delim = "\t",
                                 col_names = c("gene_name", "pathway_name"))
genes_ko_file <- read_delim("kegg/genes_ko.list",
                            delim = "\t",
                            col_names = c("gene_name", "ko_name"))
ko_pathway_file <- read_delim("kegg/ko_pathway.link",
                              delim = "\t",
                              col_names = c("pathway_name", "ko_name"))
ko_pathway_file <- ko_pathway_file %>%
  filter(!grepl("^path\\:ko",pathway_name))

pathway_file <- read_delim("kegg/pathway.list",
                           delim = "\t",
                           col_names = c("pathway_name", "pathway_name_long"))

df <- tibble(pathway_name_long = unique(pathway_file$pathway_name_long))
for (sample_name in c("L1", "L5", "L2", "L3", "PE1", "PE5", "PE2", "PE3", "PS1", "PS5", "PS2", "PS3"))
{
  print(sample_name)
  sample <- read_delim(paste0("diamond/", sample_name, ".out.gz"),
                       delim = "\t", col_names = FALSE)
  
  recruitment <- read_delim(paste0("mapped/", sample_name, "/abundance.tsv.gz"),
                            delim = "\t",
                            col_names = TRUE)
  recruitment <- recruitment %>%
    select(gene_id = target_id, tpm)
  
  protein_derep <- read_delim(paste0("derep/", sample_name, "_protein_ms_derep.tsv.gz"),
                              delim = "\t", col_names = c("seqcounts", "annotation_long"))
  protein_derep <- protein_derep %>%
    separate(annotation_long, into = c("gene_id", "func", "taxonomy"), sep = "\\|", extra = "drop")
  
  z <- sample %>%
    select(contig_id = X1, gene_name = X2) %>%
    left_join(genes_ko_file) %>%
    left_join(ko_pathway_file) %>%
    left_join(pathway_file) %>%
    select(contig_id, pathway_name_long) %>%
    filter(!is.na(pathway_name_long)) %>%
    arrange(pathway_name_long) %>%
    left_join(protein_derep, by = c("contig_id" = "seqcounts")) %>%
    left_join(recruitment) %>%
    mutate(tpm = if_else(tpm == 0, 1e-6, tpm))
  
  print(sample_name)
  print(sum(z$tpm))
  
  y <- z %>%
    group_by(pathway_name_long) %>%
    summarise(tpm = sum(tpm)) %>%
    rename(!!sample_name := tpm)
  
  df <- df %>%
    left_join(y)
}

dfx <- df %>%
  replace(., is.na(.), 0) %>%
  mutate(sum_values = L1 + L2 + L3 + L5 + PE1 + PE2 + PE3 + PE5 + PS1 + PS2 + PS3 + PS5) %>%
  arrange(desc(sum_values)) %>%
  filter(!(pathway_name_long %in% 
             c("Metabolic pathways",
               "Biosynthesis of secondary metabolites",
               "Microbial metabolism in diverse environments",
               "Biosynthesis of antibiotics",
               "Carbon metabolism",
               "2-Oxocarboxylic acid metabolism",
               "Fatty acid metabolism",
               "Biosynthesis of amino acids",
               "Degradation of aromatic compounds"))) %>%
  column_to_rownames("pathway_name_long") %>%
  select(-sum_values)

mat <- as.matrix(dfx)

mat <- mat[c(1:50), ]

pwr_trans<-function(x, trans = 2){ 
  x<- ifelse(x>0,x^(1/trans),0)
  return(x)
}

mat_sqr <- pwr_trans(x = mat, trans = 2)

col_vec <- c("#F0F8FF", "#00BFFF", "#191970")
col_fun = circlize::colorRamp2(c(0, max(mat_sqr)/2, max(mat_sqr)), col_vec)
ht_sqr <- Heatmap(mat_sqr,
                  col = col_fun,
                  border = TRUE,
                  cluster_rows = FALSE,
                  rect_gp = gpar(col = "black"),
                  heatmap_legend_param = list(
                    title = "gene counts",
                    direction = "horizontal"))
draw(ht_sqr, heatmap_legend_side = "bottom")

