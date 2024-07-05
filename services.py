import math
import pandas as pd
from typing import List


class Enter(object):
    stack_eng = 'qwertyuiopasdfghjklzxcvbnm'
    stack_rus = 'йцукенгшщзхъфывапролджэячсмитьбю'
    stack_sym = '-_!~()'
    stack_dig = '0123456789'
    allowed_symbs_default = [x for x in stack_eng] + [x for x in stack_rus] + [x for x in stack_sym] + \
                            [x for x in stack_dig] + [x for x in ' ']
    allowed_symbs_dates = [x for x in stack_dig] + [x for x in ' .,:;-/_*`~|']

    @staticmethod
    def mapped_ints(self):
        replace = [',', '.', ';']
        enter = str(' ') + str(input(self)) + str(' ')  # brace with spacebars for extra step in trimming
        #  Works with a dash, f.e. entering '7-10' returns 7, 8, 9, 10
        while enter.find('-') >= 0:
            dash_index = enter.find('-')
            dash_border_left = ''
            i_left = dash_index
            while i_left >= 0:
                if len(str(dash_border_left)) > 0 and str(enter[i_left]) not in [str(x) for x in Enter.stack_dig]:
                    break
                try:
                    sym = int(enter[i_left])
                    dash_border_left = str(sym) + str(dash_border_left)
                    dash_border_left = int(dash_border_left)
                except:
                    pass
                i_left = i_left - 1
            dash_border_right = ''
            for i_right in range(dash_index, len(enter)):
                if len(str(dash_border_right)) > 0 and str(enter[i_right]) not in [str(x) for x in Enter.stack_dig]:
                    break
                try:
                    sym = int(enter[i_right])
                    dash_border_right = str(dash_border_right) + str(sym)
                    dash_border_right = int(dash_border_right)
                except:
                    pass
            enter_updated = str(enter[:i_left])
            for every_int in range(dash_border_left, dash_border_right+1):
                enter_updated = str(enter_updated) + str(', ') + str(every_int)
            enter_updated = str(enter_updated) + str(', ') + str(enter[i_right:])
            enter = enter_updated
        for char in replace:
            enter = enter.replace(char, ' ')
        ls = list(map(int, enter.split()))
        ls = [x for x in ls]
        return ls

    # @staticmethod
    # def mapped_ints_UPDATE(self):  ## NEED TO DEBUG AND ADD DASHES
    #     replace = [',', '.', ';']
    #     symbs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    #     txt = str(input(self))
    #     while txt.find('-') >= 0:
    #         i = txt.find('-')
    #         head = txt[:i]
    #         head_space = head[::-1].find(' ')  # doesn't work if you set a space before dash
    #         if head_space < 0:
    #             head_space = 0
    #         head_index = len(head) - head_space
    #         start = txt[head_index-1:i]
    #         tail = txt[i + 1:]
    #         tail_space = tail.find(' ')
    #         if tail_space < 0:
    #             tail_space = 0
    #         tail_index = i + 1 + tail_space
    #         end = txt[i + 1: tail_index+1]
    #         try:
    #             the_range = list(range(int(start), int(end)+1))
    #             if int(end) < int(start):
    #                 the_range = ' '
    #         except:
    #             the_range = ' '
    #         txt = txt[:head_index-1] + ' ' + ' '.join(str(x) for x in the_range) + ' ' + txt[tail_index+1:] + ' '
    #     for char in replace:
    #         txt = txt.replace(char, ' ')
    #     return list(map(int, txt.split()))

    def int(input_descripton, arg_error=None, arg_min=None, arg_max=None, arg_isnt=None):
        while True:
            try:
                i = int(input(input_descripton))
                if Enter.arg_min_f(i, arg_min) is False or Enter.arg_max_f(i, arg_max) is False \
                        or Enter.arg_isnt_f(i, arg_isnt) is False:
                    print(arg_error)
                    continue
                return i
            except:
                print(arg_error)
                continue

    def float(input_descripton, arg_error=None, arg_min=None, arg_max=None, arg_isnt_in_list=None):
        while True:
            try:
                i = float(input(input_descripton))
                if Enter.arg_min_f(i, arg_min) is False or Enter.arg_max_f(i, arg_max) is False \
                        or Enter.arg_isnt_in_list_f(i, arg_isnt_in_list) is False:
                    print(arg_error)
                    continue
                return i
            except:
                print(arg_error)
                continue

    def str(input_descripton, arg_error=None, arg_min=None, arg_max=None, arg_isnt_in_list=None,
            arg_must_be: list = None, arg_max_capacity: int = None):
        while True:
            try:
                i = str(input(input_descripton))
                if Enter.arg_min_f(i, arg_min) is False or Enter.arg_max_f(i, arg_max) is False \
                        or Enter.arg_isnt_in_list_f(i, arg_isnt_in_list) is False \
                        or Enter.arg_must_be(i, arg_must_be) is False or len(i) > arg_max_capacity:
                    print(arg_error)
                    continue
                return i
            except:
                print(arg_error)
                continue


    def date(input_descripton='', arg_error=None, arg_min=None, arg_max=None, arg_isnt_in_list=None,
             arg_must_be: list = None, arg_max_capacity: int = None, replacing_symbol='.',
             format='%d.%m.%y', dayfirst: bool = True, convert_to_pd: bool = True, return_timestamp: bool = True,
             one_year_status: bool = False, one_year: str = None):
        while True:
            try:
                i = str(input(input_descripton))
                if Enter.arg_min_f(i, arg_min) is False or Enter.arg_max_f(i, arg_max) is False \
                        or Enter.arg_isnt_in_list_f(i, arg_isnt_in_list) is False \
                        or Enter.arg_must_be(i, arg_must_be) is False or len(i) > arg_max_capacity:
                    print(arg_error)
                    continue
                replace_list = ['.', ',', ':', ';', '-', '/', ' ', '_', '*', '`', '~', '|']
                for char in replace_list:
                    i = i.replace(char, replacing_symbol)
                if one_year_status is True:
                    i = i + replacing_symbol + one_year
                if convert_to_pd is True:
                    if return_timestamp is True:
                        return pd.to_datetime(i, dayfirst=dayfirst)
                    else:
                        return pd.to_datetime(i, dayfirst=dayfirst).strftime(format)
                else:
                    return i
            except:
                print(arg_error)
                continue


    @staticmethod
    def mapped_dates(self):
        replace = [',', ':', ';', '-', '/', ' ', '_', '*', '`', '~', '|']
        enter = str(input(self))
        for char in replace:
            enter = enter.replace(char, '.')
        return enter

    def arg_must_be(i, arg):
        if arg is not None:
            if isinstance(arg, (list, tuple)):
                for el in str(i).lower():
                    if str(el) in arg:
                        continue
                    else:
                        a = False
                        break
                else:
                    a = True
                return a
            elif i != arg:
                return False
        else:
            return True

    def arg_min_f(i, arg):
        if arg is not None:
            if i < arg:
                return False
        else:
            return True

    def arg_max_f(i, arg):
        if arg is not None:
            if i > arg:
                return False
        else:
            return True

    def arg_isnt_f(i, arg):
        if arg is not None:
            if i == arg or arg is True:
                return False
        else:
            return True

    def arg_isnt_in_list_f(i, arg):
        if arg is not None:
            if isinstance(arg, (list, tuple)):
                for el in arg:
                    if el == i:
                        return False
            elif i == arg or arg is True:
                return False
        else:
            return True



class Digits_operator(object):
    def find_number_of_digits(dgt):
        dgt = abs(dgt)
        counter = 0
        if dgt <= 0:
            return counter
        else:
            counter += 1
            return Digits_operator.find_number_of_digits(dgt // 10)

    def find_digits_and_print_them_out(dgt, lst):
        dgt = abs(int(dgt))
        lst = list(lst)
        if dgt <= 0:
            return lst
        else:
            lst.append(int(dgt % 10))
            return Digits_operator.find_digits_and_print_them_out(dgt // 10, lst)


class Trimmer(object):
    def left(string, amount):
        return string[:amount]

    def right(string, amount):
        return string[-amount:]


class Rus(object):
    def cases(dgt: float, one, two, five):
        x = math.trunc(abs(float(dgt)))
        if 5 <= x <= 20:
            return five
        elif (x % 10) == 1:
            return one
        elif (x % 10) == 2 or (x % 10) == 3 or (x % 10) == 4:
            return two
        else:
            return five


def question(quest: str, yes='', no='', other=''):
    """
    :rtype: object, str
    """
    answer = str(input(f'  {quest}  ')).lower()
    answer_list = {
            'yes': ['yes', 'ye', 'yeah', 'ok', 'y', 'да', 'ага', 'ок', 'хорошо', 'давай', 'го', 'д', 'lf', 'da', 'нуы'],
            'no': ['no', 'nope', 'nah', 'n', 'нет', 'не', 'не надо', 'н', 'не-а', 'yt', 'ytn', 'тщ', 'ne', 'net']}
    if answer in answer_list['yes']:
        return yes
    elif answer in answer_list['no']:
        return no
    else:
        return other


class Out:
    @staticmethod
    def reconfigure_encoding():
        import sys
        sys.stdin.reconfigure(encoding='utf-8')
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    @staticmethod
    def clear_future_warning():
        import warnings
        warnings.simplefilter(action='ignore', category=FutureWarning)
