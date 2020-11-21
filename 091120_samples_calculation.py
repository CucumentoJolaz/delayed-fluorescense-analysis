import csv

import numpy as np
from lmfit import Model
import matplotlib.pyplot as plt
from scipy.integrate import quad


def get_args(dict_args):
    a = dict_args['a']
    tau = dict_args['tau1']
    c = dict_args['c']
    return (a, tau, c)


def second_order_p_type(t, a=1, T10=1, b=1):
    return a * (T10 / (1 + b * T10 * t)) ** 2


def first_order_p_type(t, a=1, T10=1, b=1):
    return a * (T10 / (1 + b * T10 * t))


def mixed_order_model(t, T10=1, a=1, b=1, const=1):
    return const * (a / (np.exp(a * t) * (a / T10 + b) - b)) ** 2


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
ph_x = [];
ph_y = [];
ph_HC_x = [];
ph_HC_y = [];
dl_fl_x = [];
dl_fl_y = []
for i in range(NUM_OF_EXP):
    ph_x.append([]);
    ph_y.append([])
    ph_HC_x.append([]);
    ph_HC_y.append([])
    dl_fl_x.append([]);
    dl_fl_y.append([])

with open(FILENAME) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    count = 0
    # чтение CSV файла в массив
    for row in readCSV:

        if count >= 0:
            dl_fl_index = 0
            for col in range(0, NUM_OF_EXP * 2, 1):
                if (row[col]):
                    if col % 2:
                        dl_fl_y[dl_fl_index].append(float(row[col].replace(',', '.')))
                        dl_fl_index += 1
                    else:
                        dl_fl_x[dl_fl_index].append(float(row[col].replace(',', '.')))

            ph_index = 0
            for col in range(NUM_OF_EXP * 2, NUM_OF_EXP * 4, 1):
                if (row[col]):
                    if col % 2:
                        ph_y[ph_index].append(float(row[col].replace(',', '.')))
                        ph_index += 1
                    else:
                        ph_x[ph_index].append(float(row[col].replace(',', '.')))

            ph_HC_index = 0
            for col in range(NUM_OF_EXP * 4, NUM_OF_EXP * 6, 1):
                if (row[col]):
                    if col % 2:
                        ph_HC_y[ph_HC_index].append(float(row[col].replace(',', '.')))
                        ph_HC_index += 1
                    else:
                        ph_HC_x[ph_HC_index].append(float(row[col].replace(',', '.')))

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
                                                    t=ph_HC_x[i],
                                                    a=10,
                                                    tau1=1))

# Массивы для хранения названий
sample_name = ["0,015",
               "0,010",
               "0,008",
               "0,004",
               ]
ph_x_lin = np.linspace(0, 10, 10000);
ph_y_lin = []
for i in range(NUM_OF_EXP):
    ph_y_lin.append([])

ph_x_HC_lin = np.linspace(0, 10, 10000);
ph_y_HC_lin = []
for i in range(NUM_OF_EXP):
    ph_y_HC_lin.append([])

dl_fl_x_lin = np.linspace(0, 6, 6000);
dl_fl_y_lin = []
for i in range(NUM_OF_EXP):
    dl_fl_y_lin.append([])

for j in range(NUM_OF_EXP):
    a = result_dl_fl_sing_exp[j].best_values['a']
    tau = result_dl_fl_sing_exp[j].best_values['tau1']
    c = result_dl_fl_sing_exp[j].best_values['c']
    for i in dl_fl_x_lin:
        dl_fl_y_lin[j].append(single_exponential(t=i, a=a, tau1=tau, c=c))

    a = result_ph_sing_exp[j].best_values['a']
    tau = result_ph_sing_exp[j].best_values['tau1']
    c = result_ph_sing_exp[j].best_values['c']
    for i in ph_x_lin:
        ph_y_lin[j].append(single_exponential(t=i, a=a, tau1=tau, c=c))

    a = result_ph_HC_sing_exp[j].best_values['a']
    tau = result_ph_HC_sing_exp[j].best_values['tau1']
    c = result_ph_HC_sing_exp[j].best_values['c']
    for i in ph_x_lin:
        ph_y_HC_lin[j].append(single_exponential(t=i, a=a, tau1=tau, c=c))

# Построение фиттингов для замедленной флуоресценции
plt.figure(1)

#plt.title("Delayed fluorescence")
plt.plot([], [], ' ', label="Соотношение\n(моль нафталина)/(моль циклодекстрина)")
plt.axis([0, 6, 0, 90])
for i in range(NUM_OF_EXP):
    plt.plot(dl_fl_x[i], dl_fl_y[i], label=sample_name[i], linewidth=0.5)
    plt.plot(dl_fl_x_lin, dl_fl_y_lin[i], label=sample_name[i] + " fit", linewidth=0.5)
plt.xlabel("Время, с")
plt.title("Интенсивность, отн. ед.",
           loc = 'left',
          fontsize = 'medium')
plt.legend(loc='best')
filename = "Delayed fluorescence 2" + ".png"
plt.savefig(filename)

plt.figure(2)
#plt.title("Phosphorescence")
plt.plot([], [], ' ', label="Соотношение\n(моль нафталина)/(моль циклодекстрина)")
plt.axis([0, 10, 0, 50])

for i in range(NUM_OF_EXP):
    plt.plot(ph_x[i], ph_y[i], label=sample_name[i], linewidth=0.5)
    plt.plot(ph_x_lin, ph_y_lin[i], label=sample_name[i] + " fit", linewidth=0.5)
plt.xlabel("Время, с")
plt.title("Интенсивность, отн. ед.",
           loc = 'left',
          fontsize = 'medium')
plt.legend(loc='best')
filename = "Phosphorescence 2" + ".png"
plt.savefig(filename)

plt.figure(3)
#plt.title("Phosphorescence with dark filter HC-9")
plt.plot([], [], ' ', label="Соотношение\n(моль нафталина)/(моль циклодекстрина)")
plt.axis([0, 10, 0, 700])

for i in range(NUM_OF_EXP):
    plt.plot(ph_HC_x[i], ph_HC_y[i], label=sample_name[i], linewidth=0.5)
    #plt.plot(ph_x_HC_lin, ph_y_HC_lin[i], label=sample_name[i] + " fit", linewidth=0.5)
plt.xlabel("Время, с")
plt.title("Интенсивность, отн. ед.",
           loc = 'left',
          fontsize = 'medium')
plt.legend(loc='best')

filename = "Phosphorescence with HC 2" + ".png"
plt.savefig(filename)
plt.show()

ph_integr = np.zeros(NUM_OF_EXP + 1);
ph_HC_integr = np.zeros(NUM_OF_EXP + 1);
dl_fl_integr = np.zeros(NUM_OF_EXP + 1)
fl_ph_ratio = np.zeros(NUM_OF_EXP + 1)
fl_ph_HC_ratio = np.zeros(NUM_OF_EXP + 1)
ph_HC_integr_10 = np.zeros(NUM_OF_EXP + 1)
ph_HC_norm = np.zeros(NUM_OF_EXP + 1)
fl_norm = np.zeros(NUM_OF_EXP + 1)
ph_notnorm = np.zeros(NUM_OF_EXP + 1)
HC_9_koef = 50

for i in range(NUM_OF_EXP):
    ph_integr[i] = quad(single_exponential, 0, 10, args=get_args(result_ph_sing_exp[i].best_values))[0]
    ph_HC_integr[i] = quad(single_exponential, 0, 10, args=get_args(result_ph_HC_sing_exp[i].best_values))[0]
    dl_fl_integr[i] = quad(single_exponential, 0, 6, args=get_args(result_dl_fl_sing_exp[i].best_values))[0]
    ph_notnorm[i] = ph_HC_integr[i] ** 2
    #print(ph_HC_integr[i], "a", ph_notnorm[i] )
    ph_HC_integr_10[i] = ph_HC_integr[i]/10
    if i == 0:
        ph_int_max = ph_HC_integr[0]
        fl_int_max = dl_fl_integr[0]
    ph_HC_norm[i] = ph_HC_integr[i]/ph_int_max
    fl_norm[i] = dl_fl_integr[i]/fl_int_max



ph_HC_norm[0] = 0.99
naph_conc = [0.015, 0.010, 0.008, 0.004, 0,
             ]

CELLS_NUM_AROUND = 12
x = np.arange(0,0.05,0.001)
y = np.zeros(len(x))

for i in range(len(x)):
	y[i] = x[i]*(1 - (1 - x[i])**CELLS_NUM_AROUND)

f = open("out_1.txt", 'w')
f.write("naph_conc; ph_HC_integr; dl_fl_integr; \n")

for i in range(NUM_OF_EXP+1):
    f.write("{}; {}; {}; \n".format(naph_conc[i],ph_HC_integr[i],dl_fl_integr[i]))
f.close()

plt.figure(5)
#plt.title("Delayed fluorescence - phosphorescence intensity ratio")
#plt.plot([], [], ' ', label="Number of solution, naph/b-CD")
#plt.axis([0, 0.017, 0, 0.0028])
plt.plot(ph_notnorm, dl_fl_integr, '-o')
#plt.plot(x, y, '-', linewidth = 0.8, label = "Предполагаемая форма зависимости")
plt.legend(loc='best')
filename = "dlfl_ph_ratio" + ".png"
plt.xlabel("Квадрат интеральной интенсивности фософресценции, отн. ед.")
plt.title("Интегральная интенсивность замедленной флуоресценции, отн. ед.",
           loc = 'left',
          fontsize = 'medium')
plt.grid(True)
plt.savefig(filename)
plt.show()

plt.figure(6)
plt.axis([0, 0.017 , 0, 1.05])
plt.plot(naph_conc, ph_HC_norm, '-o', label = "Интегральная интенсивность\n фосфоресценции, отн. ед")
plt.plot(naph_conc, fl_norm, '-o', label = "Интегральная интенсивность\n замедленной флуоресценции, отн. ед")
plt.legend(loc='best')
plt.xlabel("Соотношение (моль нафталина)/(моль b-CD)")
plt.title("Интенсивность, отн. ед.",
           loc = 'left',
          fontsize = 'medium')
filename = "Integral intensities" + ".png"
plt.grid(True)
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
