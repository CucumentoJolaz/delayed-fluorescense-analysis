import csv

from numpy import exp, loadtxt, pi, sqrt
from lmfit import Model
import matplotlib.pyplot as plt


def second_order_p_type(t, a=1, T10=1, b=1):
    return a * (T10 / (1 + b * T10 * t)) ** 2


def first_order_p_type(t, a=1, T10=1, b=1):
    return a * (T10 / (1 + b * T10 * t))


def mixed_order_model(t, T10 = 1, a = 1, b = 1, const = 1):
    return const*(a/(exp(a*t)*(a/T10 + b) - b))**2


def exponential(t, a=1, b=1, tau1=1, tau2=1, c=1):
    e1 = 2.718 ** (-t / tau1)
    e2 = 2.718 ** (-t / tau2)
    return (a * e1 + b * e2) + c


def single_exponential(t, a=1, tau1=1, c=1):
    return a * 2.718 ** (-t / tau1) + c


class outputs:
    par_out = False

    def param_out(self, inf_src, titles_arr, iter_num=0, head="------"):
        if iter_num != 0:
            iter_num_in_func = iter_num
        else:
            iter_num_in_func = len(inf_src)

        if outputs.par_out:  # определение способа вывода данныцх  в файл
            par_out_mode = 'a'
        else:
            par_out_mode = 'w'

        with open('parameters.csv', par_out_mode) as myfile:
            myfile.write(head + '\n')
            for x in range(iter_num_in_func):
                myfile.write(titles_arr[x])
                for key, value in inf_src[x].best_values.items():
                    str_to_file = "{0} = {1:.2f}, ".format(key, value)
                    myfile.write(str_to_file)
                myfile.write("chisqr = {0:.2f}".format(inf_src[x].chisqr))
                myfile.write('\n')

            outputs.par_out = True  # если в ходе программы данная функция была выхвана хоть один раз, и при этом был создан файл с параметрами, то в дальнейшем параметры будут вноситься в этот файл с концеа, а не перезаписываться
        myfile.close()


NUM_OF_EXP = 4
FILENAME = "Sheet1.csv"
ph_x = ph_y = ph_HC_x = ph_HC_y = dl_fl_x = dl_fl_y = []
for i in range(NUM_OF_EXP) :
    ph_x.append([]); ph_y.append([])
    ph_HC_x.append([]); ph_HC_y.append([])
    dl_fl_x.append([]); dl_fl_y.append([])



with open(FILENAME) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    count = 0
    #чтение CSV файла в массив
    for row in readCSV:

        if count >= 0:
            dl_fl_index = 0
            for col in range(0, NUM_OF_EXP*2, 1):
                if (row[col]):
                    if col % 2:
                        dl_fl_y[dl_fl_index].append(float(row[col].replace(',','.')))
                        dl_fl_index += 1
                    else:
                        dl_fl_x[dl_fl_index].append(float(row[col].replace(',','.')))

            ph_index = 0
            for col in range(NUM_OF_EXP*2, NUM_OF_EXP*4, 1):
                if (row[col]):
                    if col % 2:
                        ph_y[ph_index].append(float(row[col].replace(',','.')))
                        ph_index += 1
                    else:
                        ph_x[ph_index].append(float(row[col].replace(',','.')))

            ph_HC_index = 0
            for col in range(NUM_OF_EXP*4, NUM_OF_EXP*6, 1):
                if (row[col]):
                    if col % 2:
                        ph_HC_y[ph_HC_index].append(float(row[col].replace(',','.')))
                        ph_index += 1
                    else:
                        ph_HC_x[ph_HC_index].append(float(row[col].replace(',','.')))
        count += 1


# создание модели для фитинга
result_dl_fl_sing_exp = []
result_ph_sing_exp = []
result_ph_HC_sing_exp = []

sing_exp_model = Model(single_exponential)

for i in range(NUM_OF_EXP):

    result_dl_fl_sing_exp.append(sing_exp_model.fit(dl_fl_y[i],
                                                    t=dl_fl_x[i],
                                                    a=1,
                                                    tau1=1))
    result_ph_sing_exp.append(sing_exp_model.fit(ph_y[i],
                                                 t=ph_x[i],
                                                 a=1,
                                                 tau1=1))
    result_ph_HC_sing_exp.append(sing_exp_model.fit(ph_HC_y[i],
                                                 t=ph_x[i],
                                                 a=1,
                                                 tau1=1))


# Массивы для хранения названий
sample_name = ["091120.01, 0,015",
               "091120.02, 0,010",
               "091120.03, 0,008",
               "091120.04, 0,004",
               ]

# Построение фиттингов для замедленной флуоресценции
plt.figure(1)

plt.title("Delayed fluorescence")
plt.plot([], [], ' ', label="Number of solution, naph/b-CD")
for i in range(NUM_OF_EXP):
    plt.plot(dl_fl_x[i], dl_fl_y[i], label=sample_name[i])
    #plt.plot(dl_fl_x[i], result_dl_fl_sing_exp[i].best_fit, label=sample_name[i] + " fit", linewidth=0.5)
plt.legend(loc='best')
filename = "Delayed fluorescence"+ ".png"
plt.savefig(filename)


plt.figure(2)
plt.title("Phosphorescence")
plt.plot([], [], ' ', label="Number of solution, naph/b-CD")
for i in range(NUM_OF_EXP):
    plt.plot(ph_x[i], ph_y[i], label=sample_name[i])
    plt.plot(ph_x[i], result_ph_sing_exp[i].best_fit, label=sample_name[i] + " fit", linewidth=0.5)
plt.legend(loc='best')
filename = "Phosphorescence"+ ".png"
plt.savefig(filename)


plt.figure(3)
plt.title("Phosphorescence with dark filter HC-9")
plt.plot([], [], ' ', label="Number of solution, naph/b-CD")
for i in range(NUM_OF_EXP):
    plt.plot(ph_HC_x[i], ph_HC_y[i], label=sample_name[i])
    plt.plot(ph_HC_x[i], result_ph_HC_sing_exp[i].best_fit, label=sample_name[i] + " fit", linewidth=0.5)
plt.legend(loc='best')
filename = "Phosphorescence with HC"+ ".png"
plt.savefig(filename)

plt.show()

# Запись файла с параметрами
# out_obj = outputs()
#
# out_obj.param_out(result_bi_exp,
#                   common_name,
#                   NUM_OF_EXP,
#                   "The best fitted parameters for biexponential model for delayed fluorescence")
#
# out_obj.param_out(result_dl_fl_sing_exp,
#                   common_name,
#                   NUM_OF_EXP,
#                   "The best fitted parameters for monoexponential model for delayed fluorescence")
#
# out_obj.param_out(result_mix_ord,
#                   common_name,
#                   NUM_OF_EXP,
#                   "The best fitted parameters for mixed order model for delayed fluorescence")
#
# out_obj.param_out(result_ph_sing_exp,
#                   common_name,
#                   NUM_OF_EXP,
#                   "The best fitted parameters for exponential model for phosphorescence")
