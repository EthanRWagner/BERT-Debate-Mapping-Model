from re import T
import pandas as pd
import csv

def main() -> None:
    #open old workbook
    from_workbook = pd.read_excel('Argument Position.xlsx')
    from_workbook.head()

    #Create a list of lists that has format [[<topic>, <statement>, <truth value>], ...]
    topics = []
    arguments = []
    t_values = []

    #separate statements
    for i in range(len(from_workbook['<Topic>'])):
        j= 0

        set = from_workbook['<Statement>'].iloc[i]
        reformatted_set = ""
        inside_stat = False
        blank = False
        for chars in set:
            uni = ord(chars)
            if uni != 123 and uni != 125 and uni != 10:
                if blank and uni != 34:
                    continue
                blank = False
                if uni == 34:
                    inside_stat = ~inside_stat
                elif uni == 44 and not inside_stat:
                    reformatted_set = reformatted_set + '\n'
                    blank = True
                else:
                    reformatted_set = reformatted_set + chars
        splt_args = reformatted_set.split('\n')
        for arg in splt_args:
            arguments.append(arg)
            j+=1

        if j < 6 or j > 10:
            print("Argument Error!\n")
            print(i)
            exit(0)

        #separate topics
        topic = from_workbook['<Topic>'].iloc[i]
        for _ in range(j):
            topics.append(topic)

        #separate truth values
        truths = from_workbook['<Truth Value>'].iloc[i]
        # set = from_workbook['<Truth Value>'].iloc[0]
        t = 0
        for vals in truths:
            uni = ord(vals)
            if uni == 70:
                t_values.append('NEGATIVE')
                t += 1
            elif uni == 84:
                t_values.append('AFFIRMATIVE')
                t += 1

        if t != j:
            print(i, "\nlook at truth value set.\n")
            print(splt_args)
            exit(0)

    if len(topics) != len(arguments) != len(t_values):
        print(len(topics))
        print(len(arguments))
        print(len(t_values))
        print("Length error\n")
        exit(0)

    #make new workbook
    to_workbook = pd.DataFrame({'Topic': topics, 'Statement': arguments, 'Truth Value': t_values})
    to_workbook.to_excel('Final Argument Position Data.xlsx')
    print("Done!\n")

if __name__ == "__main__":
    main()