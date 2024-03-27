use std::fs;

#[derive(Debug, Clone)]
struct Aliment {
    id: usize,
    weight: usize,
    score: usize,
}

#[derive(Debug, Clone)]
struct Decision {
    f1: Vec<usize>,
    f0: Vec<usize>,
    l: Vec<usize>,
}

impl Decision {
    fn new(f1: Vec<usize>, f0: Vec<usize>, l: Vec<usize>) -> Self {
        Decision { f1, f0, l }
    }

    fn weight_f1_total(&self, aliment_list: &[Aliment]) -> usize {
        self.f1.iter().map(|&id| aliment_list.iter().find(|a| a.id == id).unwrap().weight).sum()
    }

    fn score_eval(&self, aliment_list: &[Aliment]) -> usize {
        let mut score = 0;

        for &id in &self.f1 {
            score += aliment_list.iter().find(|a| a.id == id).unwrap().score;
        }

        for &id in &self.l {
            score += aliment_list.iter().find(|a| a.id == id).unwrap().score;
        }

        score
    }
}

fn branch_bound(decision: Decision, best: usize, aliment_list: &[Aliment]) -> usize {
    let mut best = best;
    let mut count_eval = 0;
    let mut count_constraint = 0;

    if decision.weight_f1_total(aliment_list) <= WMAX {
        let score = decision.score_eval(aliment_list);

        if decision.l.is_empty() {
            if score > best {
                best = score;
            }
        } else {
            if score > best {
                let x = decision.l[0].clone();
                let mut decision1 = decision.clone();
                decision1.f1.push(x);
                let mut decision2 = decision.clone();
                decision2.f0.push(x);

                let best1 = branch_bound(decision1, best, aliment_list);
                let best2 = branch_bound(decision2, best, aliment_list);
                best = best1.max(best2);
            } else {
                count_eval += 1;
            }
        }
    } else {
        count_constraint += 1;
    }

    best
}

const FILE_NAME: &str = "Instances/inst35obj.txt";

fn get_value_in_txt(file_name: &str) -> (usize, usize, Vec<Aliment>) {
    let contents = fs::read_to_string(file_name).expect("Error reading the file");
    let mut lines = contents.lines();

    let init: Vec<usize> = lines.next().unwrap().split_whitespace().map(|s| s.parse().unwrap()).collect();
    let n = init[0];
    let w_max = init[1];

    let aliment_list: Vec<Aliment> = lines
        .map(|line| {
            let values: Vec<usize> = line.split_whitespace().map(|s| s.parse().unwrap()).collect();
            Aliment {
                id: values[0],
                weight: values[1],
                score: values[2],
            }
        })
        .collect();

    (n, w_max, aliment_list)
}

const WMAX: usize = 112;

fn main() {
    let (n, w_max, aliment_list) = get_value_in_txt(FILE_NAME);

    let count_constraint = 0;
    let count_eval = 0;

    let decision = Decision::new(
        vec![],
        vec![],
        aliment_list.iter().map(|aliment| aliment.id).collect(),
    );

    println!("Fin: {}", branch_bound(decision, 0, &aliment_list));
}
