def main(tpr, fpr):
    p = 50
    n = 25
    recall = tpr / 100
    tp = (tpr * p) / 100
    fn = p - tp
    tn = (100 - fpr) * n / 100
    fp = n - tn
    precision = tp / (tp + fp)
    f1 = 2 * ((precision * recall)/(precision + recall))
    p4 = (4 * tp * tn)/(4 * tp * tn + (tp + tn)*(fp + fn))
    print(f'tp:{tpr} fp:{fpr} - f1:{round(f1,3)} p4:{round(p4,3)}')
    return

if __name__ == '__main__':
    l =  [(91.8,52.7),(77.8,47.2),(91.2,53.1) 
        ,(84.8,52.7),(90.8,47.2),(89.2,53.1)
        ,(92,52.7),(74,47.2),(88.6,53.1)
        ,(90.2,52.7),(91.2,47.2),(89.2,53.1)
        ,(91.4,52.7),(90.2,47.2),(92,53.1)]
        

    for i in l:
        main(i[0],i[1])