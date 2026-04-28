import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math as m

if 'coef_size' not in st.session_state:
    st.session_state.coef_size = 1.0

if 'manual_scale' not in st.session_state:
    st.session_state.manual_scale = False


def size_down():
    st.session_state.coef_size -= 0.1
    st.session_state.manual_scale = True


def size_up():
    st.session_state.coef_size += 0.1
    st.session_state.manual_scale = True


if 'language' not in st.session_state:
    st.session_state.language = 0


def click_grid_button():
    st.session_state.button_grid = not st.session_state.button_grid


if 'button_grid' not in st.session_state:
    st.session_state.button_grid = False


def click_grid_button():
    st.session_state.button_grid = not st.session_state.button_grid


if 'button_table' not in st.session_state:
    st.session_state.button_table = False


def click_table_button():
    st.session_state.button_table = not st.session_state.button_table


if 'button_feature' not in st.session_state:
    st.session_state.button_feature = False


def click_button_feature():
    st.session_state.button_feature = not st.session_state.button_feature


if "func_nulls" not in st.session_state:
    st.session_state.func_nulls = None

if "E_section" not in st.session_state:
    st.session_state.E_section = None

if "even_feature" not in st.session_state:
    st.session_state.even_feature = None

if "func_choice_index" not in st.session_state:
    st.session_state.func_choice_index = 0

if "picked_color" not in st.session_state:
    st.session_state.picked_color = "#FF1313"


def reset_features():
    st.session_state.func_nulls = None
    st.session_state.E_section = None
    st.session_state.even_feature = None
    st.session_state.manual_scale = False


def convert_for_saving(df):
    return df.to_csv(index=False).encode("utf-8")


st.set_page_config(layout="wide")

funcs_list = ["y = sin(x)", "y = cos(x)", "y = tan(x)", "y = ctn(x)", "y = ax + c",
              "y = ax^2 + bx + c", "y = ln(x)"]

language_list = {"func_choice": ["Выбор функции:", "Choose function:"],
                 "accuracy": ["Погрешность", "Accuracy:"],
                 "file_get": ["Взять данные из файла", "Take data from a file:"],
                 "save_button": ["Сохранить...", "Save...:"],
                 "choose_language": ["Выборя языка:", "Choose language:"],
                 "color_choose": ["Выбор цвета графика:", "Choose graphic color:"],
                 "table": ["Таблица", "Table"],
                 "features": ["Свойства", "Features"],
                 "show_grid": ["Убрать/Вернуть сетку", "Remove/Show grid"],
                 "size": ["Масштаб:", "Size:"],
                 "ref": ["Подсказка", "Reference"]
                 }

features_rus = {"y = sin(x)": "Область определения (D): x∈R (все действительные числа)\n"
                              "Множество значений (E): [−1;1]\n"
                              "Четность/Нечетность: Нечетная (sin(−x)=−sin(x))\n"
                              "Периодичность: Периодическая, наименьший период T=2π\n"
                              "Нули: x=πn,n∈Z\n",
                "y = cos(x)": "Область определения (D): x∈R (все действительные числа)\n"
                              "Множество значений (E): [−1;1]\n"
                              "Четность/Нечетность: Четная (cos(−x) = cos(x))\n"
                              "Периодичность: Периодическая, наименьший период T=2π\n"
                              "Нули: x=π/2 + πn,n∈Z\n",
                "y = tan(x)": "Область определения (D): Все x кроме x = π/2 + πn,n∈Z"
                              "Множество значений (E): R (все действительные числа)\n"
                              "Четность/Нечетность: Нечетная (tan(−x) = -tan(x))\n"
                              "Периодичность: Периодическая, наименьший период T=π\n"
                              "Нули: x=πn,n∈Z\n",
                "y = ctn(x)": "Область определения (D): Все x кроме x = πn,n∈Z"
                              "Множество значений (E): R (все действительные числа)\n"
                              "Четность/Нечетность: Нечетная (tan(−x) = -tan(x))\n"
                              "Периодичность: Периодическая, наименьший период T=π\n"
                              "Нули: x=π/2 + πn,n∈Z\n",
                "y = ax + c": "Область определения (D): x∈R (все действительные числа)\n"
                              "Множество значений (E): [−1;1]\n"
                              f"Нули: {st.session_state.func_nulls}\n",
                "y = ax^2 + bx + c": "Область определения (D): x∈R (все действительные числа)\n"
                                     f"Множество значений (E): {st.session_state.E_section}\n"
                                     f"Четность/Нечетность: {st.session_state.even_feature}\n"
                                     f"Нули: {st.session_state.func_nulls}\n",
                "y = ln(x)": "Область определения (D): x>0 (строго положительный числа)\n"
                             f"Множество значений (E): x∈R (все действительные числа)\n"
                             f"Нули: x = 1\n",
                }

features_eng = {
    "y = sin(x)": "Domain (D): x∈R (all real numbers)\nRange (E): [−1;1]\nParity: Odd (sin(−x)=−sin(x))\nPeriodicity: Periodic, fundamental period T=2π\nZeros: x=πn, n∈Z\n",
    "y = cos(x)": "Domain (D): x∈R (all real numbers)\nRange (E): [−1;1]\nParity: Even (cos(−x)=cos(x))\nPeriodicity: Periodic, fundamental period T=2π\nZeros: x=π/2 + πn, n∈Z\n",
    "y = tan(x)": "Domain (D): All x except x = π/2 + πn, n∈Z\nRange (E): R (all real numbers)\nParity: Odd (tan(−x) = -tan(x))\nPeriodicity: Periodic, fundamental period T=π\nZeros: x=πn, n∈Z\n",
    "y = ctn(x)": "Domain (D): All x except x = πn, n∈Z\nRange (E): R (all real numbers)\nParity: Odd (cot(−x) = -cot(x))\nPeriodicity: Periodic, fundamental period T=π\nZeros: x=π/2 + πn, n∈Z\n",
    "y = ax + c": f"Domain (D): x∈R (all real numbers)\nRange (E): [−1;1]\nZeros: {st.session_state.func_nulls}\n",
    "y = ax^2 + bx + c": f"Domain (D): x∈R (all real numbers)\nRange (E): {st.session_state.E_section}\nParity: {st.session_state.even_feature}\nZeros: {st.session_state.func_nulls}\n",
    "y = ln(x)": "Domain (D): x>0 (strictly positive numbers)\nRange (E): x∈R (all real numbers)\nZeros: x = 1\n"
}

main_col_1, main_col_2, main_col_3 = st.columns([0.2, 0.65, 0.15], gap="small")

x_func_val = np.array([])
y_func_val = np.array([])
func_val = pd.DataFrame()

with main_col_3:
    lan_list = ["Русский", "English"]

    chosen_lan = st.menu_button(label=language_list["choose_language"][st.session_state.language],
                                key="lang_choice",
                                options=lan_list,
                                width="stretch")

    if chosen_lan == "Русский":
        st.session_state.language = 0
        st.rerun()

    if chosen_lan == "English":
        st.session_state.language = 1
        st.rerun()

with main_col_1:
    func_choice_val = st.selectbox(label=language_list["func_choice"][st.session_state.language],
                                   options=funcs_list,
                                   on_change=reset_features,
                                   index=st.session_state.func_choice_index,
                                   placeholder="...",
                                   key="func_choice", )

    st.session_state.func_choice_index = funcs_list.index(func_choice_val)

    cont_tab_terms = st.container(border=True)

    accuracy_val = cont_tab_terms.number_input(label="",
                                               step=0.1,
                                               key="accuracy_val",
                                               value=None,
                                               placeholder=language_list["accuracy"][st.session_state.language],
                                               label_visibility="collapsed")

    tab_placeholder = cont_tab_terms.empty()

    sub_col_1, sub_col_2, sub_col_3 = tab_placeholder.columns(3, gap="xsmall")

    start_tab = sub_col_1.number_input(label="",
                                       step=0.1,
                                       key="start_tab",
                                       value=None,
                                       placeholder="x0",
                                       label_visibility="collapsed")
    step_tab = sub_col_2.number_input(label="",
                                      step=0.1,
                                      key="step_tab",
                                      value=None,
                                      placeholder="xh",
                                      label_visibility="collapsed")
    end_tab = sub_col_3.number_input(label="",
                                     step=0.1,
                                     key="end_tab",
                                     value=None,
                                     placeholder="xn",
                                     label_visibility="collapsed")

    if start_tab is not None and end_tab is not None and step_tab is not None and step_tab > 0:
        x_func_val = np.arange(start_tab, end_tab, step_tab, dtype=np.float64)

    if accuracy_val:
        len_accuracy = int(len(str(accuracy_val)[2:]))
        if not (len_accuracy):
            np.set_printoptions(precision=0)
        else:
            np.set_printoptions(precision=len_accuracy)

    match func_choice_val:
        case "y = sin(x)":

            y_func_val = np.sin(x_func_val)

        case "y = cos(x)":

            y_func_val = np.cos(x_func_val)

        case "y = tan(x)":
            if x_func_val.size > 0:
                y_func_val = np.tan(x_func_val)
                y_func_val = np.where(np.isfinite(y_func_val), y_func_val, np.nan)
                if len(y_func_val) > 1:
                    dy = np.diff(y_func_val)
                    jump_indices = np.where(np.abs(dy) > 100)[0]
                    y_func_val[jump_indices] = np.nan
                    y_func_val[jump_indices + 1] = np.nan

        case "y = ctn(x)":
            if x_func_val.size > 0:
                y_func_val = 1 / np.tan(x_func_val)
                y_func_val = np.where(np.isfinite(y_func_val), y_func_val, np.nan)
                if len(y_func_val) > 1:
                    dy = np.diff(y_func_val)
                    jump_indices = np.where(np.abs(dy) > 100)[0]
                    y_func_val[jump_indices] = np.nan
                    y_func_val[jump_indices + 1] = np.nan

        case "y = ax + c":

            sub_col_1, sub_col_2 = cont_tab_terms.columns(2, gap="xsmall")

            a_val = sub_col_1.number_input(label="",
                                           step=0.1,
                                           format="%0.1f",
                                           key="a_val_pow_1",
                                           placeholder="a",
                                           value=None,
                                           label_visibility="collapsed")

            c_val = sub_col_2.number_input(label="",
                                           step=0.1,
                                           format="%0.1f",
                                           key="c_val_pow_1",
                                           placeholder="c",
                                           value=None,
                                           label_visibility="collapsed")
            if a_val is not None and c_val is not None:
                y_func_val = a_val * x_func_val + c_val
                if not (st.session_state.func_nulls):
                    if a_val > 0:
                        st.session_state.func_nulls = -c_val / a_val
                    elif a_val == 0 and c_val != 0:
                        st.session_state.func_nulls = "Нулей нет"
                    elif a_val == 0 and c_val == 0:
                        st.session_state.func_nulls = "Вся числовая прямая"
                    st.rerun()

        case "y = ax^2 + bx + c":

            sub_col_1, sub_col_2, sub_col_3 = cont_tab_terms.columns(3, gap="xsmall")

            a_val = sub_col_1.number_input(label="",
                                           step=0.1,
                                           format="%0.1f",
                                           key="a_val_pow_2",
                                           placeholder="a",
                                           value=None,
                                           label_visibility="collapsed")

            b_val = sub_col_2.number_input(label="",
                                           step=0.1,
                                           format="%0.1f",
                                           key="b_val_pow_2",
                                           placeholder="b",
                                           value=None,
                                           label_visibility="collapsed")
            c_val = sub_col_3.number_input(label="",
                                           step=0.1,
                                           format="%0.1f",
                                           key="c_val_pow_2",
                                           placeholder="c",
                                           value=None,
                                           label_visibility="collapsed")

            if a_val is not None and b_val is not None and c_val is not None:
                y_func_val = a_val * x_func_val ** 2 + b_val * x_func_val + c_val
                dis = b_val ** 2 - 4 * a_val * c_val
                if not (st.session_state.func_nulls):
                    if dis > 0:
                        st.session_state.func_nulls = f"{(-b_val + m.sqrt(dis)) / (2 * a_val)}, {(-b_val - m.sqrt(dis)) / (2 * a_val)}"
                    if dis == 0:
                        st.session_state.func_nulls = -b_val / (2 * a_val)
                    else:
                        st.session_state.func_nulls = "Нет нулей"
                    st.rerun()
                if not (st.session_state.E_section):
                    if a_val > 0:
                        st.session_state.E_section = f"[{(4 * a_val * c_val - b_val ** 2) / (4 * a_val)}; +∞]"
                    else:
                        st.session_state.E_section = f"[-∞; {(4 * a_val * c_val - b_val ** 2) / (4 * a_val)}]"
                    st.rerun()
                if not (st.session_state.even_feature):
                    if b_val == 0:
                        st.session_state.even_feature = "четная"
                    else:
                        st.session_state.even_feature = "общего вида"
                    st.rerun()

        case "y = ln(x)":
            if x_func_val.size > 0:
                y_func_val = np.log(x_func_val)
                y_func_val = np.where(np.isfinite(y_func_val), y_func_val, np.nan)
            else:
                y_func_val = np.array([])

    st.space("stretch")

    table_placeholder = st.empty()

    feature_placeholder = st.empty()

with main_col_3:
    cont_app_terms = st.container(border=True)

    picked_color = cont_app_terms.color_picker(label=language_list["color_choose"][st.session_state.language],
                                               value=st.session_state.picked_color,
                                               key="color_picker")

    st.session_state.picked_color = picked_color

    grid_button = cont_app_terms.button(label=language_list["show_grid"][st.session_state.language],
                                        key="grid_button",
                                        on_click=click_grid_button,
                                        width="stretch")

    tabel_button = st.button(label=language_list["table"][st.session_state.language],
                             key="table_button",
                             on_click=click_table_button,
                             width="stretch")

    features_button = st.button(label=language_list["features"][st.session_state.language],
                                key="features_button",
                                on_click=click_button_feature,
                                width="stretch")


    @st.dialog(language_list["ref"][st.session_state.language])
    def ref():
        if not (st.session_state.language):
            st.markdown("1. Выберите функцию:")
            st.markdown("В выпадающем списке \"Выбор функции\" выберите из предложенного списка функцию для табуляции.")
            st.markdown("2. Укажите границы табуляции:")
            st.markdown("В полях x0 (начало), xh (шаг), xn (конец) задайте интервал для вычисления таблицы значений.")
            st.markdown("3. Посмотрите таблицу:")
            st.markdown(
                "После ввода данных нажмите кнопку \"Таблица\" — отобразятся значения x и y в указанном диапазоне.")
            st.markdown("4. Изучите свойства функции:")
            st.markdown(
                "В блоке \"Свойства\" автоматически показаны: область определения, множество значений, чётность, периодичность, нули. "
                "Вызывается это окно при помощи кнопки \"Свойства\".")
            st.markdown("5. Настройте график:")
            st.markdown("Измените цвет линии через палитру.")
            st.markdown("6. Включите/выключите сетку кнопкой \"Убрать/Вернуть сетку\".")
            st.markdown("7. Выберите язык интерфейса с помощбю выпадающего окна \"Выбора языка\".")
            st.markdown("8. Оцените погрешность:")
            st.markdown("При необходимости введите допустимую погрешность вычислений в соответствующее поле.")
        else:
            st.markdown("1. Select a function:")
            st.markdown("In the \"Function selection\" dropdown, choose a function from the list to tabulate.")
            st.markdown("2. Specify tabulation boundaries:")
            st.markdown(
                "In the fields x0 (start), xh (step), xn (end), set the interval for calculating the table of values.")
            st.markdown("3. View the table:")
            st.markdown(
                "After entering the data, click the \"Table\" button — the x and y values for the specified range will be displayed.")
            st.markdown("4. Study the function properties:")
            st.markdown(
                "In the \"Properties\" block, the following are automatically shown: domain, range, parity, periodicity, zeros. "
                "This window is opened using the \"Properties\" button.")
            st.markdown("5. Adjust the graph:")
            st.markdown("Change the line color using the color palette.")
            st.markdown("6. Toggle the grid on/off using the \"Show/Hide grid\" button.")
            st.markdown("7. Select the interface language using the \"Language selection\" dropdown.")
            st.markdown("8. Estimate the error:")
            st.markdown("If necessary, enter the permissible calculation error in the corresponding field.")


    reference_button = st.button(label=language_list["ref"][st.session_state.language],
                                 key="reference_button",
                                 width="stretch")

    if reference_button:
        ref()

graph_fig, ax = plt.subplots(facecolor=(.0588, .0667, .0863), figsize=(15, 9.4))

if x_func_val.size == y_func_val.size and x_func_val.size > 0:
    ax.plot(x_func_val,
            y_func_val,
            color=picked_color)
    func_val = pd.DataFrame({"x": x_func_val, "y": y_func_val})

ax.tick_params(labelcolor=picked_color)

graph_fig.set_size_inches(15, 13.5)

if st.session_state.button_grid:
    ax.grid()

# Логика масштаба: авто по границам ИЛИ ручной через coef_size
use_auto_scale = not st.session_state.manual_scale and start_tab is not None and end_tab is not None and start_tab != end_tab

if use_auto_scale:
    x_start, x_end = min(start_tab, end_tab), max(start_tab, end_tab)
    x_margin = (x_end - x_start) * 0.05 if x_end != x_start else 1.0
    ax.set_xlim(x_start - x_margin, x_end + x_margin)
else:
    ax.set_xlim(-10 * st.session_state.coef_size, 10 * st.session_state.coef_size)

if use_auto_scale:
    if y_func_val.size > 0 and np.any(np.isfinite(y_func_val)):
        finite_y = y_func_val[np.isfinite(y_func_val)]
        if finite_y.size > 0:
            y_min, y_max = np.min(finite_y), np.max(finite_y)
            if func_choice_val in ["y = tan(x)", "y = ctn(x)"]:
                y_range = max(abs(y_min), abs(y_max), 10)
                ax.set_ylim(-y_range * 1.1, y_range * 1.1)
            else:
                y_range = y_max - y_min if y_max != y_min else 1
                ax.set_ylim(y_min - y_range * 0.1, y_max + y_range * 0.1)
        else:
            ax.set_ylim(-10 * st.session_state.coef_size, 10 * st.session_state.coef_size)
    else:
        ax.set_ylim(-10 * st.session_state.coef_size, 10 * st.session_state.coef_size)
else:
    ax.set_ylim(-10 * st.session_state.coef_size, 10 * st.session_state.coef_size)

ax.set_facecolor((.0588, .0667, .0863))

func_val_csv = convert_for_saving(func_val) if not func_val.empty else b""

with main_col_2:
    st.pyplot(fig=graph_fig,
              clear_figure=True)

    col_1, col_2, col_3, col_4 = st.columns([0.6, 0.25, 0.1, 0.1], gap="small")

    save_button = col_1.download_button(label=language_list["save_button"][st.session_state.language],
                                        key="save_button",
                                        width=150,
                                        data=func_val_csv,
                                        file_name="TAB_DATA.csv",
                                        mime="text/csv")

    size_markdown = col_2.markdown(language_list["size"][st.session_state.language],
                                   text_alignment="right")

    size_down_button = col_3.button(label=" + ",
                                    key="size_up_button",
                                    width=50)
    size_up_button = col_4.button(label=" - ",
                                  key="size_down_button",
                                  width=50)

    if size_up_button:
        size_up()

    if size_down_button:
        size_down()

with main_col_1:
    if st.session_state.button_table:
        table_tab = table_placeholder.container(border=True, height="stretch")

        table_tab.dataframe(func_val,
                            height=244,
                            hide_index=True)
    else:
        table_placeholder.empty()

    if st.session_state.button_feature:
        feature_tab = feature_placeholder.container(border=True, height="stretch")

        if not (st.session_state.language):
            feature_tab.write(features_rus[func_choice_val])
        else:
            feature_tab.write(features_eng[func_choice_val])

    else:
        feature_placeholder.empty()
