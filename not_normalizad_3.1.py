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

ph_x = [[], [], [], []]
ph_y = [[], [], [], []]
dl_fl_x = [[], [], [], []]
dl_fl_y = [[], [], [], []]
with open('lt.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    count = 0
    #чтение CSV файла в массив
    for row in readCSV:
        if count >= 19 and count < 991:


            dl_fl_index = 0
            for col in range(NUM_OF_EXP*2, NUM_OF_EXP*4, 1):
                if col % 2:
                    dl_fl_y[dl_fl_index].append(float(row[col]))
                    dl_fl_index += 1
                else:
                    dl_fl_x[dl_fl_index].append(float(row[col]))


        if count >= 12 and count < 984:

            ph_index = 0

            for col in range(0, NUM_OF_EXP*2, 1):

                if col % 2:
                    ph_y[ph_index].append(float(row[col]))
                    ph_index += 1
                else:
                    ph_x[ph_index].append(float(row[col]))


        count += 1







# создание модели для фитинга
result_bi_exp = []
result_dl_fl_sing_exp = []

result_ph_sing_exp = []
result_mix_ord = []

for i in range(NUM_OF_EXP):
    bi_exp_model = Model(exponential)
    result_bi_exp.append(
        bi_exp_model.fit(dl_fl_y[i],
                         t=dl_fl_x[0],
                         a=10,
                         b=10,
                         tau1=1,
                         tau2=10,
                         c = 1))  # рассчёт трёх видов фиттинга

    sing_exp_model = Model(single_exponential)
    result_dl_fl_sing_exp.append(sing_exp_model.fit(dl_fl_y[i],
                                                    t=dl_fl_x[0],
                                                    a=10,
                                                    tau1=1))

    mix_ord_model = Model(mixed_order_model)
    result_mix_ord.append(sing_exp_model.fit(dl_fl_y[i],
                                             t=dl_fl_x[0],))


for i in range(NUM_OF_EXP):
    sing_exp_model = Model(single_exponential)
    result_ph_sing_exp.append(sing_exp_model.fit(ph_y[i],
                                                 t=ph_x[0],
                                                 a=10,
                                                 tau1=1))

# Массивы для хранения названий фитов
common_name = ["50 flashes ",
               "40 flashes ",
               "30 flashes ",
               "20 flashes ",
               ]
common_name.reverse()

# Построение фиттингов для замедленной флуоресценции
for i in range(NUM_OF_EXP):
    plt.figure(i)
    plt.title("Delayed fluorescence " + common_name[-i - 1])

    plt.plot(dl_fl_x[0], dl_fl_y[i], 'b-')
    plt.plot(dl_fl_x[0], result_bi_exp[i].best_fit, 'y-', label='biexponential fit', linewidth=0.5)
    plt.plot(dl_fl_x[0], result_dl_fl_sing_exp[i].best_fit, label='monoexponential fit', linewidth=0.5)
    plt.plot(dl_fl_x[0], result_mix_ord[i].best_fit, label='mixed order fit', linewidth=0.5)
    plt.legend(loc='best')
    filename = "dl_fl_fit_num" + str(i) + ".pdf"
    plt.savefig(filename)

for i in range(NUM_OF_EXP):
    plt.figure(31)

    plt.title("Exponential fits")
    plt.plot(dl_fl_x[0],
             result_dl_fl_sing_exp[i].best_fit,
             label=common_name[i] + " " + r' $\chi^2=$' + str("{0:.2f}".format(result_ph_sing_exp[i].chisqr)),
             linewidth=0.3)
    plt.legend(loc='best')
filename = "dl_fl_sing_exp_compare" + ".pdf"
plt.savefig(filename)

# биэкспоненциальная замедленная флуоресценция
for i in range(NUM_OF_EXP):
    plt.figure(7)

    plt.title("Biexponential fits")
    plt.plot(dl_fl_x[0],
             result_bi_exp[i].best_fit,
             label=common_name[i] + " " + r' $\chi^2=$' + str("{0:.2f}".format(result_bi_exp[i].chisqr)),
             linewidth=0.3)
    plt.legend(loc='best')
filename = "dl_fl_exp_compare" + ".pdf"
plt.savefig(filename)

for i in range(NUM_OF_EXP):
    plt.figure(423)

    plt.title("mixed order fits")
    plt.plot(dl_fl_x[0],
             result_mix_ord[i].best_fit,
             label=common_name[i] + " " + r' $\chi^2=$' + str("{0:.2f}".format(result_bi_exp[i].chisqr)),
             linewidth=0.3)
    plt.legend(loc='best')
filename = "dl_fl_exp_compare" + ".pdf"
plt.savefig(filename)



# Просто построение фитингов для каждого из экспериментов
for i in range(NUM_OF_EXP):
    plt.figure(i + 20)

    plt.title("Phosphorescence" + common_name[i])
    plt.plot(ph_x[0], ph_y[i], 'b-')
    plt.plot(ph_x[0], result_ph_sing_exp[i].best_fit, 'g', label='Monoexponential fit', linewidth=0.5)
    plt.legend(loc='best')
    filename = "ph_fit_num" + str(i) + ".pdf"
    plt.savefig(filename)

# моноэкспоненциальная фосфоресценция
for i in range(NUM_OF_EXP):
    plt.figure(9)

    plt.title("Monoexponential fits, phosphorescence")
    labelo = common_name[i] + " " + r' $\chi^2=$' + str("{0:.2f}".format(result_ph_sing_exp[i].chisqr))
    plt.plot(ph_x[0], result_ph_sing_exp[i].best_fit, label=labelo, linewidth=0.3)
    plt.legend(loc='best')
filename = "ph_sing_exp_compare" + ".pdf"
plt.savefig(filename)

# Запись файла с параметрами
out_obj = outputs()

out_obj.param_out(result_bi_exp,
                  common_name,
                  NUM_OF_EXP,
                  "The best fitted parameters for biexponential model for delayed fluorescence")

out_obj.param_out(result_dl_fl_sing_exp,
                  common_name,
                  NUM_OF_EXP,
                  "The best fitted parameters for monoexponential model for delayed fluorescence")

out_obj.param_out(result_mix_ord,
                  common_name,
                  NUM_OF_EXP,
                  "The best fitted parameters for mixed order model for delayed fluorescence")

out_obj.param_out(result_ph_sing_exp,
                  common_name,
                  NUM_OF_EXP,
                  "The best fitted parameters for exponential model for phosphorescence")
