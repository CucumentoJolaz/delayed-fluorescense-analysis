import csv

from numpy import exp, loadtxt, pi, sqrt
from lmfit import Model
import matplotlib.pyplot as plt



def second_order_p_type(t, a = 1, T10= 1, b= 1):
    return a * (T10 / (1 + b * T10 * t)) ** 2


def first_order_p_type(t, a= 1, T10= 1, b= 1):
    return a * (T10 / (1 + b * T10 * t))


def exponential(t, a= 1, b= 1, tau1= 1, tau2= 1):
    e1 = 2.718 ** (-t / tau1)
    e2 = 2.718 ** (-t / tau2)
    return (a * e1 + b * e2)

def single_exponential(t, a= 1, tau1= 1):
    return a*2.718**(-t/tau1)

def fits(x, y):
    second_or_model = Model(second_order_p_type)
    result_sec_or = second_or_model.fit(y, t=x, a=1, T10=1, b=1)
    print(result_sec_or.fit_report())

    first_or_model = Model(first_order_p_type)
    result_first_or = first_or_model.fit(y, t=x, a=1, T10=1, b=1)
    print(result_first_or.fit_report())

    be_exp_model = Model(exponential)
    result_biexp = be_exp_model.fit(y, t=x, a=1, b=1, tau1=1, tau2=1)
    print(result_biexp.fit_report())

    plt.plot(x, y, 'bo')
    # plt.plot(x, result.init_fit, 'k--', label='initial fit')
    plt.plot(x, result_sec_or.best_fit, 'r', label='second order fit')
    plt.plot(x, result_first_or.best_fit, 'g', label='first order fit')
    plt.plot(x, result_biexp.best_fit, 'b', label='biexponential fit')


with open('dNCDch_lt.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    ph_x = [[], [], [], [], [], []]
    ph_y = [[], [], [], [], [], []]
    dl_fl_x = [[], [], [], [], [], [], []]
    dl_fl_y = [[], [], [], [], [], [], []]

    count = 0

    for row in readCSV:
        if count >= 19 and count < 991:
            dl_fl_index = 0
            for col in range(31, 45, 1):
                if col % 2:
                    dl_fl_y[dl_fl_index].append(float(row[col]))
                else:
                    dl_fl_x[dl_fl_index].append(float(row[col]))
                    dl_fl_index += 1

        if count >= 12 and count < 984:
            ph_index = 0
            for col in range(19, 31, 1):
                if col % 2:
                    ph_y[ph_index].append(float(row[col]))
                else:
                    ph_x[ph_index].append(float((row[col])))
                    ph_index += 1
        count += 1

ph_y_max = []
dl_fl_y_max = []

# поиск максимумов
for x in range(6):
    ph_y_max.append(max(ph_y[x]))
for x in range(7):
    dl_fl_y_max.append(max(dl_fl_y[x]))

# нормировка

ph_y_norm = [[], [], [], [], [], []]
dl_fl_y_norm = [[], [], [], [], [], [], []]

for x in range(len(dl_fl_y[0])):
    for y in range(len(ph_y_max)):
        ph_y_n_var = (ph_y[y][x]) / ph_y_max[y]
        ph_y_norm[y].append(ph_y_n_var)

    for y in range(len(dl_fl_y_max)):
        dl_fl_y_n_var = (dl_fl_y[y][x]) / dl_fl_y_max[y]
        dl_fl_y_norm[y].append(dl_fl_y_n_var)

csv_arr = []
csv_arr.append(ph_x[0])

for x in range(len(ph_y_norm)):
    csv_arr.append(ph_y_norm[x])

csv_arr.append(dl_fl_x[0])

for x in range(len(dl_fl_y_norm)):
    csv_arr.append(dl_fl_y_norm[x])

# print(csv_arr)
# сохранение нормализованных данных в файл
with open('normalized.csv', 'w') as myfile:
    for y in range(len(csv_arr[0])):
        for x in range(len(csv_arr)):
            myfile.write(str(csv_arr[x][y]))
            myfile.write(" ")
        myfile.write('\n')
myfile.close()

# создание модели для фитинга

data = loadtxt('normalized.csv')
x = data[:, 7]
y = data[:, 8]
# tet_f, k_p, T10, b

result_sec_or = []
result_first_or = []
result_bi_exp = []
result_dl_fl_sing_exp = []

result_ph_sing_exp = []
result_ph_bi_exp = []

for i in range(7):
    second_or_model = Model(second_order_p_type)
    result_sec_or.append(second_or_model.fit(dl_fl_y_norm[i], t=x, a=10, T10=1, b=10))
    #  print(result_sec_or[i].fit_report())

    first_or_model = Model(first_order_p_type)
    result_first_or.append(first_or_model.fit(dl_fl_y_norm[i], t=x, a=10, T10=1, b=10))
    # print(result_first_or[i].fit_report())

    bi_exp_model = Model(exponential)
    result_bi_exp.append(bi_exp_model.fit(dl_fl_y_norm[i], t=x, a=10, b=10, tau1=1, tau2=10)) # рассчёт трёх видов фиттинга

    sing_exp_model = Model(single_exponential)
    result_dl_fl_sing_exp.append(sing_exp_model.fit(dl_fl_y_norm[i], t=x, a=10, tau1=1))


for i in range(6):
    bi_exp_model = Model(exponential)
    result_ph_bi_exp.append(bi_exp_model.fit(ph_y_norm[i], t=ph_x[0], a=10, b=10, tau1=1, tau2=10))

    sing_exp_model = Model(single_exponential)
    result_ph_sing_exp.append(sing_exp_model.fit(ph_y_norm[i], t=ph_x[0], a=10, tau1=1))

#Массивы для хранения названий фитов
common_name = ["50 flashes ",
               "40 flashes ",
               "30 flashes ",
               "20 flashes ",
               "10 flashes ",
               "5 flashes ",
               ]
#Название линий для фитинга второго поряднка
res_sec_or_name = ["50 flashes " + r'$\chi^2=$' + str("{0:.2f}".format(result_sec_or[0].chisqr)),
                   "40 flashes " + r'$\chi^2=$' + str("{0:.2f}".format(result_sec_or[1].chisqr)),
                   "30 flashes " + r'$\chi^2=$' + str("{0:.2f}".format(result_sec_or[2].chisqr)),
                   "20 flashes " + r'$\chi^2=$' + str("{0:.2f}".format(result_sec_or[3].chisqr)),
                   "10 flashes " + r'$\chi^2=$' + str("{0:.2f}".format(result_sec_or[4].chisqr)),
                   "5 flashes " + r'$\chi^2=$' + str("{0:.2f}".format(result_sec_or[5].chisqr))]

res_bi_exp_name = ["50 flashes " + r'$\chi^2=$' + str("{0:.2f}".format(result_bi_exp[0].chisqr)),
                   "40 flashes " + r'$\chi^2=$' + str("{0:.2f}".format(result_bi_exp[1].chisqr)),
                   "30 flashes " + r'$\chi^2=$' + str("{0:.2f}".format(result_bi_exp[2].chisqr)),
                   "20 flashes " + r'$\chi^2=$' + str("{0:.2f}".format(result_bi_exp[3].chisqr)),
                   "10 flashes " + r'$\chi^2=$' + str("{0:.2f}".format(result_bi_exp[4].chisqr)),
                   "5 flashes " + r'$\chi^2=$' + str("{0:.2f}".format(result_bi_exp[5].chisqr))]


#Построение фиттингов для замедленной флуоресценции
for i in range(6):
    plt.figure(i)
    plt.title("Delayed fluorescence " + common_name[i])
    plt.plot(x, dl_fl_y_norm[i], 'b-')
    plt.plot(x, result_bi_exp[i].best_fit, 'y-', label='biexponential fit', linewidth = 0.5)
    plt.plot(x, result_dl_fl_sing_exp[i].best_fit, label='monoexponential fit', linewidth=0.5)
    plt.legend(loc='best')
    filename = "dl_fl_fit_num_" + str(i) + ".pdf"
    plt.savefig(filename)



for i in range(6):
    plt.figure(31)
    plt.title("Exponential fits")
    plt.plot(x, result_dl_fl_sing_exp[i].best_fit,  label=res_sec_or_name[i] , linewidth = 0.3)
    plt.legend(loc='best')
filename = "dl_fl_sing_exp_compare" + ".pdf"
plt.savefig(filename)

#биэкспоненциальная замедленная флуоресценция
for i in range(6):
    plt.figure(7)
    plt.title("Biexponential fits")
    plt.plot(x, result_bi_exp[i].best_fit,  label=res_bi_exp_name[i], linewidth = 0.3)
    plt.legend(loc='best')

filename = "dl_fl_exp_compare" + ".pdf"
plt.savefig(filename)

for i in range(6):
    plt.figure(10)
    plt.title("Second order fits")
    plt.plot(x, result_sec_or[i].best_fit,  label=res_sec_or_name[i] , linewidth = 0.3)
    plt.legend(loc='best')
filename = "dl_fl_sec_ord_compare" + ".pdf"
plt.savefig(filename)

#Просто построение фитингов для каждого из экспериментов
for i in range(6):
    plt.figure(i + 20)
    plt.title("Phosphorescence" + common_name[-i - 1])
    plt.plot(ph_x[0], ph_y_norm[i], 'b-')
    plt.plot(ph_x[0], result_ph_sing_exp[i].best_fit, 'g', label='Monoexponential fit', linewidth = 0.5)
    plt.plot(ph_x[0], result_ph_bi_exp[i].best_fit, 'y-', label='Biexponential fit', linewidth = 0.5)
    plt.legend(loc='best')
    filename = "ph_fit_num_" + str(i) + ".pdf"
    plt.savefig(filename)

#биэкспоненциальная фосфоресценция
for i in range(6):
    plt.figure(8)
    plt.title("Biexponential fits, phosphorescence")
    labelo = common_name[-i-1] + " "+ r' $\chi^2=$'+ str("{0:.2f}".format(result_ph_bi_exp[i].chisqr))
    plt.plot(ph_x[0], result_ph_bi_exp[i].best_fit,  label=labelo, linewidth = 0.3)
    plt.legend(loc='best')

filename = "ph_bi_exp_compare" + ".pdf"
plt.savefig(filename)
#моноэкспоненциальная фосфоресценция
for i in range(6):
    plt.figure(9)
    plt.title("Monoexponential fits, phosphorescence")
    labelo = common_name[-i - 1] + " " + r' $\chi^2=$'+ str("{0:.2f}".format(result_ph_sing_exp[i].chisqr))
    plt.plot(ph_x[0], result_ph_sing_exp[i].best_fit,  label=labelo, linewidth = 0.3)
    plt.legend(loc='best')
filename = "ph_sing_exp_compare" + ".pdf"
plt.savefig(filename)




def param_out(inf_src, titles_arr, iter_num = 0, head = "------",):
    if iter_num != 0:
        iter_num_in_func = iter_num
    else:
        iter_num_in_func = len(inf_src)
    with open('parameters.csv', 'w') as myfile:
        myfile.write(head + '\n')
        for x in range(iter_num_in_func):
            myfile.write(titles_arr[x])
            for key, value in inf_src[x].best_values.items():
                str_to_file = "{0} = {1:.2f}, ".format(key, value)
                myfile.write(str_to_file)
            myfile.write("chisqr = {0:.2f}".format(inf_src[x].chisqr))
            myfile.write('\n')
    myfile.close()

#Запись файла с параметрами

param_out(result_bi_exp, common_name, 6 ,"The best fitted parameters for biexponential model for delayed fluorescence")
param_out(result_dl_fl_sing_exp, common_name,6, "The best fitted parameters for monoexponential model for delayed fluorescence")
common_name.reverse()
param_out(result_ph_sing_exp, common_name,6, "The best fitted parameters for exponential model for phosphorescence")

myfile.close()
#plt.show()

