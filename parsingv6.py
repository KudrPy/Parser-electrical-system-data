
import numpy as np
import matplotlib.pyplot as plt


class Parser():

    def __init__(self, path_cfg, path_dat ):
            self.path_cfg = path_cfg
            self.path_dat = path_dat
            self.matrix_analog = None
            self.count_digital = None
            self.count_analog = None
            self.matrix_digital = None
            self.matrix_analog_cfg = None
            self.names_analog_signal = None
            self.names_digital_signal = None
            self.number = None
            self.index_row = None
            self.index_element = None
            self.element = None
            self.index_pars = None
            self.value_list = None
            self.value_dict_for_voltage = None
            self.degrees_list = None
            self.value_dict_for_degrees = None
            self.discrete_list = None
            self.value_dict_for_discretes = None
            self.data_list_discrete = None
            self.t1 = None

    def inform_data(self):
            name_file = self.path_cfg
            with open(name_file, "r") as file:
                config = file.readlines()
                print("Конфигурация =", config[0])
                sign = config[1].split(",")
                print(config[1])
                count_signals = sign[0]
                count_analog = sign[1].split("A")[0]
                self.count_analog = int(count_analog)
                count_digital = sign[2].split("D")[0]
                self.count_digital = int(count_digital)
                print(f"Количество сигналов:{count_signals}\n"
                      f"Количество аналоговых сигналов:{count_analog}\n"
                      f"Количество дискретных сигналов:{count_digital}")

    def parse_cfg(self):
            cfg_file = self.path_cfg
            names_analog_signal = []
            with open(cfg_file, "r") as f1:
                dlina_cfg = f1.readlines()[2:self.count_analog + 2]
                for index_row1 in range(len(dlina_cfg)):
                    row_cfg = dlina_cfg[index_row1]
                    filter_data = self.__filter(row_cfg)
                    split_row_cfg = filter_data.split(",")
                    names_analog_signal.append(split_row_cfg[1].upper())
                self.matrix_analog_cfg = np.zeros((len(dlina_cfg), len(split_row_cfg) - 6))
                print(self.matrix_analog_cfg.shape)
                for index_row1 in range(len(dlina_cfg)):
                    row_cfg = dlina_cfg[index_row1]
                    split_row_cfg = row_cfg.split(",")
                    for index_element_cfg in range(5, len(split_row_cfg) - 1):
                        element_cfg = split_row_cfg[index_element_cfg]
                        self.matrix_analog_cfg[index_row1, index_element_cfg - 5] = element_cfg

    def parse_data(self):
            data = []
            dat_file = self.path_dat
            with open(dat_file, "r") as f:
                dlina = f.readlines()
                for index_row in range(len(dlina)):
                    row = dlina[index_row]
                    split_row = row.split(",")
                self.matrix_analog = np.zeros((len(dlina), len(split_row)))
                print(self.matrix_analog.shape)
                for index_row in range(len(dlina)):
                    row = dlina[index_row]
                    split_row = row.split(",")
                    for index_element in range(len(split_row)):
                        element = split_row[index_element]
                        self.matrix_analog[index_row, index_element] = element

    def get_data(self,number):
            return self.matrix_analog[:,number]

    def __filter(self, list_data):
            filter_data = list_data.split(" ")
            end_data = ""
            for one_element in filter_data:
                end_data = end_data + one_element
            return end_data

    def parse_analog(self):
            data1 = []
            cfg_file = self.path_cfg
            self.names_analog_signal = []
            with open(cfg_file, "r") as f1:
                dlina_cfg = f1.readlines()[2:self.count_analog + 2]
                for index_row1 in range(len(dlina_cfg)):
                    row_cfg = dlina_cfg[index_row1]
                    filter_data = self.__filter(row_cfg)
                    split_row_cfg = filter_data.split(",")
                    self.names_analog_signal.append(split_row_cfg[1].upper())
                matrix_analog_cfg = np.zeros((len(dlina_cfg), len(split_row_cfg) - 6))
                print(matrix_analog_cfg.shape)
                for index_row1 in range(len(dlina_cfg)):
                    row_cfg = dlina_cfg[index_row1]
                    split_row_cfg = row_cfg.split(",")
                    for index_element_cfg in range(5, len(split_row_cfg) - 1):
                        element_cfg = split_row_cfg[index_element_cfg]
                        self.matrix_analog_cfg[index_row1, index_element_cfg - 5] = element_cfg

    def parse_digital(self):
            self.names_digital_signal = []
            cfg_file = self.path_cfg
            with open(cfg_file, "r") as f1:
                dlina_cfg_digital = f1.readlines()[self.count_analog + 2:self.count_analog + self.count_digital + 2]
                for index_row2 in range(len(dlina_cfg_digital)):
                    row_cfg2 = dlina_cfg_digital[index_row2]
                    filter_data2 = self.__filter(row_cfg2)
                    split_row_cfg2 = filter_data2.split(",")
                    self.names_digital_signal.append(split_row_cfg2[1].upper())
                matrix_digital_cfg = np.zeros((len(dlina_cfg_digital), len(split_row_cfg2)))
                for index_row2 in range(len(dlina_cfg_digital)):
                    row_cfg2 = dlina_cfg_digital[index_row2]
                    split_row_cfg2 = row_cfg2.split(",")
                    for index_element_cfg2 in range(0, 1):
                        element_cfg2 = split_row_cfg2[index_element_cfg2]
                        matrix_digital_cfg[index_row2, index_element_cfg2] = element_cfg2

    def names_for_voltage(self):
            voltages = ["Ud_A_bus1:A1", "Ud_B_bus1:A2", "Ud_C_bus1:A3", "Ud_A_line1:A4", "Ud_B_line1:A5", "Ud_C_line1:A6"]
            self.value_dict_for_voltage = {}
            for voltage in voltages:
                index = self.names_analog_signal.index(voltage.upper()) + 2
                data_list_voltages = self.get_data(index)
                value_list = []
                a = self.matrix_analog_cfg[index - 2, 0]
                b = self.matrix_analog_cfg[index - 2, 1]
                for elem in data_list_voltages:
                    value = a * elem + b
                    value_list.append(value)

                self.value_dict_for_voltage[voltage]=value_list

    def names_for_degrees(self):
            degrees = ["Phi_A_Bus1:A7", "Phi_B_Bus1:A8", "Phi_C_Bus1:A9", "Phi_A_Line1:A10", "Phi_B_Line1:A11", "Phi_C_Line1:A12"]
            self.value_dict_for_degrees = {}
            for degree in degrees:
                index = self.names_analog_signal.index(degree.upper()) + 2
                data_list_degrees = self.get_data(index)
                degrees_list = []
                a1 = self.matrix_analog_cfg[index - 2, 0]
                b1 = self.matrix_analog_cfg[index - 2, 1]
                for elem in data_list_degrees:
                    value1 = a1 * elem + b1
                    degrees_list.append(value1)

                self.value_dict_for_degrees[degree]=degrees_list

    def names_for_discrete(self):
            discretes = ["BRK_1_41:D1", "OP14:D2", "STR14:D3","OP1VN:D4","STR1VN:D5","OP2VN:D6","STR2VN:D7","BRK1VN:D8","BRK2VN:D9"]
            self.value_dict_for_discretes = {}
            for discrete in discretes:
                index = self.names_digital_signal.index(discrete.upper()) + 14
                data_list_discrete = self.get_data(index)
                self.value_dict_for_discretes[discrete] = data_list_discrete

    def plotFigBus(self, data_Ua1, data_Ub1, data_Uc1, data_PhA1, data_PhB1, data_PhC1,name):
            data_x = self.get_data(1)
            data_x = list(map(lambda x: x*0.000001,data_x))
            fig = plt.figure()
            fig.set_figwidth(20)
            fig.set_figheight(10)
            # fig, ax = plt.subplots(2, 3, figsize=(20,10))
            ax = fig.add_subplot(231)
            ax2 = fig.add_subplot(232)
            ax3 = fig.add_subplot(233)
            ax4 = fig.add_subplot(234)
            ax5 = fig.add_subplot(235)
            ax6 = fig.add_subplot(236)
            ax.set_xlim([0, 2])
            ax.set_ylim([0, 500])
            ax.plot(data_x, data_Ua1, color="y", label='Напряжение фазы А шины')
            ax.legend(loc="best")
            ax.set_xlabel("t,c")
            ax.grid()
            ax2.plot(data_x, data_Ub1, color="g",label='Напряжение фазы B шины')
            ax2.set_xlabel("t,c")
            ax2.legend(loc="best")
            ax2.grid()
            ax3.plot(data_x, data_Uc1, color="r",label='Напряжение фазы C шины')
            ax3.set_xlabel("t,c")
            ax3.legend(loc="best")
            ax3.grid()
            ax4.plot(data_x, data_PhA1, color="y",label='Угол фазы А шины')
            ax4.set_xlabel("t,c")
            ax4.legend(loc="best")
            ax4.grid()
            ax5.plot(data_x, data_PhB1, color="g",label='Угол фазы В шины')
            ax5.set_xlabel("t,c")
            ax5.legend(loc="best")
            ax5.grid()
            ax6.plot(data_x, data_PhC1, color="r",label='Угол фазы С шины')
            ax6.set_xlabel("t,c")
            ax6.legend(loc="best")
            ax6.grid()
            plt.show()
            fig.savefig(f"C:\\Users\\1\\Desktop\\diplom3.gf42\\Rank_00001\\Run_00001\\{name}.png")

    def plotFigLine(self, data_Ua1l, data_Ub1l, data_Uc1l, data_PhA1l, data_PhB1l, data_PhC1l, name1):
            data_x = self.get_data(1)
            data_x = list(map(lambda x: x * 0.000001, data_x))
            fig = plt.figure()
            fig.set_figwidth(20)
            fig.set_figheight(10)
            ax = fig.add_subplot(231)
            ax2 = fig.add_subplot(232)
            ax3 = fig.add_subplot(233)
            ax4 = fig.add_subplot(234)
            ax5 = fig.add_subplot(235)
            ax6 = fig.add_subplot(236)
            ax.plot(data_x, data_Ua1l, color="y", label='Напряжение фазы А линии')
            ax.legend(loc="upper right")
            ax.set_xlabel("t,c")
            ax.grid()
            ax2.plot(data_x, data_Ub1l, color="g", label='Напряжение фазы B линии')
            ax2.set_xlabel("t,c")
            ax2.legend(loc="upper right")
            ax2.grid()
            ax3.plot(data_x, data_Uc1l, color="r", label='Напряжение фазы C линии')
            ax3.set_xlabel("t,c")
            ax3.legend(loc="upper right")
            ax3.grid()
            ax4.plot(data_x, data_PhA1l, color="y", label='Угол фазы А линии')
            ax4.set_xlabel("t,c")
            ax4.legend(loc="upper right")
            ax4.grid()
            ax5.plot(data_x, data_PhB1l, color="g", label='Угол фазы В линии')
            ax5.set_xlabel("t,c")
            ax5.legend(loc="upper right")
            ax5.grid()
            ax6.plot(data_x, data_PhC1l, color="r", label='Угол фазы С линии')
            ax6.set_xlabel("t,c")
            ax6.legend(loc="upper right")
            ax6.grid()
            plt.show()
            fig.savefig(f"C:\\Users\\1\\Desktop\\diplom3.gf42\\Rank_00001\\Run_00001\\{name1}.png")

    def plotFigDig(self, XCBR, OP14, STR14, OP1VN, STR1VN, OP2VN, STR2VN, BRK1VN, BRK2VN,name2):
            data_x = self.get_data(1)
            data_x = list(map(lambda x: x * 0.000001, data_x))
            fig = plt.figure()
            fig.set_figwidth(20)
            fig.set_figheight(10)
            ax = fig.add_subplot(337)
            ax2 = fig.add_subplot(334)
            ax3 = fig.add_subplot(331)
            ax4 = fig.add_subplot(335)
            ax5 = fig.add_subplot(332)
            ax6 = fig.add_subplot(336)
            ax7 = fig.add_subplot(333)
            ax8 = fig.add_subplot(338)
            ax9 = fig.add_subplot(339)
            ax.plot(data_x, XCBR, color="b", label='Положение выключателя 14')
            ax.legend(loc="best")
            ax.set_xlabel("t,c")
            ax.grid()
            ax2.plot(data_x, OP14, color="b", label='Срабатывание защиты 14')
            ax2.set_xlabel("t,c")
            ax2.legend(loc="best")
            ax2.grid()
            ax3.plot(data_x, STR14, color="b", label='Пуск защиты 14')
            ax3.set_xlabel("t,c")
            ax3.legend(loc="best")
            ax3.grid()
            ax4.plot(data_x, OP1VN, color="b", label='Срабатывание защиты 1 на ВН ПС')
            ax4.set_xlabel("t,c")
            ax4.legend(loc="best")
            ax4.grid()
            ax5.plot(data_x, STR1VN, color="b", label='Пуск защиты 1 на ВН ПС')
            ax5.set_xlabel("t,c")
            ax5.legend(loc="best")
            ax5.grid()
            ax6.plot(data_x, OP2VN, color="b", label='Срабатывание защиты 2 на ВН ПС')
            ax6.set_xlabel("t,c")
            ax6.legend(loc="best")
            ax6.grid()
            ax7.plot(data_x, STR2VN, color="b", label='Пуск защиты 2 на ВН ПС')
            ax7.set_xlabel("t,c")
            ax7.legend(loc="best")
            ax7.grid()
            ax8.plot(data_x, BRK1VN, color="b", label='Положение выключателя 1 на ВН ПС')
            ax8.set_xlabel("t,c")
            ax8.legend(loc="best")
            ax8.grid()
            ax9.plot(data_x, BRK2VN, color="b", label='Положение выключателя 2 на ВН ПС')
            ax9.set_xlabel("t,c")
            ax9.legend(loc="best")
            ax9.grid()
            plt.show()
            fig.savefig(f"C:\\Users\\1\\Desktop\\diplom3.gf42\\Rank_00001\\Run_00001\\{name2}.png")



parser = Parser("C:\\Users\\1\\Desktop\\diplom3.gf42\\Rank_00001\\Run_00001\\StartLin.cfg",
                        "C:\\Users\\1\\Desktop\\diplom3.gf42\\Rank_00001\\Run_00001\\StartLin.dat")
parser.inform_data()
parser.parse_cfg()
parser.parse_data()
parser.parse_analog()
parser.parse_digital()
parser.names_for_voltage()
parser.names_for_degrees()
parser.names_for_discrete()

Ua = "Ud_A_bus1:A1"
Ub = "Ud_B_bus1:A2"
Uc = "Ud_C_bus1:A3"
PhA = "Phi_A_Bus1:A7"
PhB = "Phi_B_Bus1:A8"
PhC = "Phi_C_Bus1:A9"
t1 = parser.get_data(1)
Ua = parser.value_dict_for_voltage["Ud_A_bus1:A1"]
Ub = parser.value_dict_for_voltage["Ud_B_bus1:A2"]
Uc = parser.value_dict_for_voltage["Ud_C_bus1:A3"]
PhA = parser.value_dict_for_degrees["Phi_A_Bus1:A7"]
PhB = parser.value_dict_for_degrees["Phi_B_Bus1:A8"]
PhC = parser.value_dict_for_degrees["Phi_C_Bus1:A9"]
parser.plotFigBus(Ua, Ub, Uc, PhA, PhB, PhC,"bus")

Ual = "Ud_A_line1:A4"
Ubl = "Ud_B_line1:A5"
Ucl = "Ud_C_line1:A6"
PhAl = "Phi_A_Line1:A10"
PhBl = "Phi_B_Line1:A11"
PhCl = "Phi_C_Line1:A12"
Ual = parser.value_dict_for_voltage["Ud_A_line1:A4"]
Ubl = parser.value_dict_for_voltage["Ud_B_line1:A5"]
Ucl = parser.value_dict_for_voltage["Ud_C_line1:A6"]
PhAl = parser.value_dict_for_degrees["Phi_A_Line1:A10"]
PhBl = parser.value_dict_for_degrees["Phi_B_Line1:A11"]
PhCl = parser.value_dict_for_degrees["Phi_C_Line1:A12"]
parser.plotFigLine(Ual, Ubl, Ucl, PhAl, PhBl, PhCl,"line")

xcbr = "BRK_1_41:D1"
op14 = "OP14:D2"
str14 = "STR14:D3"
op1VN= "OP1VN:D4"
str1VN= "STR1VN:D5"
op2VN= "OP2VN:D6"
str2VN= "STR2VN:D7"
xcbr = parser.value_dict_for_discretes["BRK_1_41:D1"]
op14 = parser.value_dict_for_discretes["OP14:D2"]
str14 = parser.value_dict_for_discretes["STR14:D3"]
op1VN = parser.value_dict_for_discretes["OP1VN:D4"]
str1VN = parser.value_dict_for_discretes["STR1VN:D5"]
op2VN = parser.value_dict_for_discretes["OP2VN:D6"]
str2VN = parser.value_dict_for_discretes["STR2VN:D7"]
BRK1VN = parser.value_dict_for_discretes["BRK1VN:D8"]
BRK2VN = parser.value_dict_for_discretes["BRK2VN:D9"]
parser.plotFigDig(xcbr, op14, str14, op1VN, str1VN, op2VN, str2VN,BRK1VN, BRK2VN, "discrete")



data_file = "C:\\Users\\1\\Desktop\\Диплом\\прогоны Comtrade\\parsingv5.py"
with open(data_file, "r") as file:





    class RSYN:
        def __init__(self, LivLinVal, LivBusVal, mode):
            self._LivLinVal = LivLinVal
            self._LivBusVal = LivBusVal
            self._mode = mode
            self._PhV_BUS = parser.value_dict_for_voltage["Ud_A_bus1:A1"]
            self._PhV_LINE = parser.value_dict_for_voltage["Ud_A_line1:A4"]

        def get_PhV_BUS(self):
            return self._PhV_BUS

        def get_PhV_LINE(self):
            return self._PhV_BUS

        def set_PhV_BUS(self, value):
            self._PhV_BUS = value

        def set_PhV_LINE(self, value):
            self._PhV_LINE = value

        def check(self):
            # 0 - слепое
            if self._mode == 0:
                return True
            if self._mode == 1:
                # 1 - КННЛ и КННШ
                for i in range(len(self._PhV_BUS)):
                    if self._PhV_BUS[i] > self._LivBusVal and self._PhV_LINE[i] > self._LivLinVal:
                        return True

            if self._mode == 2:
                # 2 - КОНЛ и КННШ
                if self._PhV_BUS > self._LivBusVal and self._PhV_LINE < self._LivLinVal:
                    return True
            if self._mode == 3:
                # 3 - КННЛ и КОНШ
                if self._PhV_BUS < self._LivBusVal and self._PhV_LINE > self._LivLinVal:
                    return True
            if self._mode == 4:
                # 4 - КННЛ и КННШ или КННЛ и КОНШ или КОНЛ и КННШ
                if self._PhV_BUS > self._LivBusVal and self._PhV_LINE > self._LivLinVal or \
                        self._PhV_BUS < self._LivBusVal and self._PhV_LINE > self._LivLinVal or \
                        self._PhV_BUS > self._LivBusVal and self._PhV_LINE < self._LivLinVal:
                    return True
                else:
                    return False


    class RREC:
        def __init__(self, wait_time):
            # self._str = False
            self._op_rrec = False
            self._syn_prg = False
            self._rel = False
            self._str_rrec = False
            self._op = None
            self._pos_brk = None
            self._time_str = None
            self._wait_time = wait_time
            self._actual_time = None

            self.state = None
            self.Waittocomplete = 0


        # def set_str(self, value):
        #     self._str = value
        #
        def get_syn_prg(self):
            return self._syn_prg

        def set_op(self, value):
            self._op = value

        def set_rel(self, value):
            self._rel = value

        def set_pos_brk(self, value):
            self._pos_brk = value

        def set_time(self, value):
            self._actual_time = value

        def wait(self):
            if (self._actual_time - self._time_str) > self._wait_time:
                self._str_rrec = False
                self._syn_prg = True

        def start(self):

            if self._rel == True:
                self._op_rrec = True

            if not self._str_rrec:
                if self._op == True and self._pos_brk == False:
                    self._time_str = self._actual_time
                    self._str_rrec = True
            else:
                self.wait()









