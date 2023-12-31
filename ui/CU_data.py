from PyQt5.QtWidgets import QDialog, QLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, pyqtSignal
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.font_manager as fm
import matplotlib.image as img
import pandas as pd
from Code.class_json import *
from ui.CU_store_data import StoreData



class DataPage(QDialog):
    year_data_signal = pyqtSignal(str)
    infra_data_signal = pyqtSignal(str)
    store_data_signal = pyqtSignal(str)
    result_data_signal = pyqtSignal(str)

    def __init__(self, clientapp, data_):
        super().__init__()
        # 기본 한글 폰트 설정
        font_path = "C:\\Users\\KDT113\\AppData\\Local\\Microsoft\\Windows\\Fonts\\TmoneyRoundWindExtraBold.ttf"
        font_name = fm.FontProperties(fname=font_path).get_name()
        plt.rc('font', family=font_name)
        loadUi('./ui_file/CU_data.ui', self)
        self.clientapp = clientapp
        self.clientapp.set_widget(self)
        self.data = data_
        self.window_option()
        self.btn_event()
        self.signal_event()
        self.population_signal()
        self.encoder = ObjEncoder()
        self.decoder = ObjDecoder()

    def signal_event(self):
        """시그널 이벤트 함수"""
        self.year_data_signal.connect(self.show_population)
        self.infra_data_signal.connect(self.show_infra)
        self.store_data_signal.connect(self.show_store)
        self.result_data_signal.connect(self.show_result)

    def btn_event(self):
        """버튼 클릭 이벤트 함수"""
        self.back_btn.clicked.connect(lambda x: self.close())
        self.back_btn_2.clicked.connect(self.population_signal)
        self.back_btn_3.clicked.connect(self.infra_signal)
        self.back_btn_4.clicked.connect(self.store_signal)
        self.back_btn_5.clicked.connect(self.result_signal)

    def create_population_plot(self, year_):
        """꺾은선 그래프 출력 함수"""
        year_data = self.decoder.binary_to_obj(year_)
        year_list = []
        year_personnel_list = []
        for year in year_data:
            year_id = year.yea_id
            years = year.yea_year
            year_list.append(years)
            year_tourist = year.yea_tourist
            if year.yea_personnel > 10000:
                year_personnel = year.yea_personnel/10000
            else:
                year_personnel = 0
            year_personnel_list.append(year_personnel)

        df1 = pd.DataFrame({'x': year_list, 'y': year_personnel_list})
        plt.plot(df1['x'], df1['y'], color='blue', alpha=0.4, linestyle='-', marker='*')

        plt.xlim((year_list[0]-1), (year_list[-1]+1))
        plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter(f'%i만'))
        plt.xlabel('년도')
        plt.ylabel('관광객 수(명)')
        plt.title("관광지 방문객 수")
        plt.xticks(range((year_list[0]), (year_list[-1]+1)))

    def create_infra_plot(self, infra_):
        """파이 그래프 출력 함수"""
        infra_data = self.decoder.binary_to_obj(infra_)
        infra_list = list()
        store = infra_data.inf_cp1
        infra_list.append(store)
        life = infra_data.inf_lf2
        infra_list.append(life)
        sch_tra = infra_data.inf_sc3
        infra_list.append(sch_tra)
        parking = infra_data.inf_pk4
        infra_list.append(parking)
        commerce = infra_data.inf_su5
        infra_list.append(commerce)
        culture = infra_data.inf_ct6
        infra_list.append(culture)
        hotel = infra_data.inf_ad7
        infra_list.append(hotel)
        health = infra_data.inf_hc8
        infra_list.append(health)
        building = infra_data.inf_bd9
        infra_list.append(building)
        dwelling = infra_data.inf_rf0
        infra_list.append(dwelling)

        infra_num_list = list()
        labels = list()
        label = ['경쟁업체', '여가시설', '교육 및 교통시설', '주차시설', '상업시설', '관광 및 문화 시설',
                 '숙박시설', '건강 및 종교시설', '빌딩', '주거시설']
        for infra, label in zip(infra_list, label):
            if infra != 0:
                infra_num_list.append(infra)
                labels.append(label)
        ratio = infra_num_list
        colors = ['#ff9999', '#ffc000', '#8fd9b6', '#d395d0', '#ffe4e1', '#faebd7', '#cbbeb5', '#f5f5dc', '#89a5ea',
                  '#ff8e7f', '#a5ea89', '#929292', '#ffcb6b', '#800000', '#59227c', '#6ccad0', '#99cc66', '#ccffff']
        wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}

        if len(infra_num_list) == 0:
            img_ = img.imread('./ui_img/텅.png')
            plt.imshow(img_)
            plt.axis('off')
        else:
            plt.pie(ratio, autopct='%.1f%%', startangle=90, counterclock=False, colors=colors,
                    wedgeprops=wedgeprops)
            plt.legend(labels, loc='center left', bbox_to_anchor=(0, 0.7))
            plt.title("매물기준 반경 330m 주변 인프라", pad=20)
            plt.axis('equal')


    def population_signal(self):
        """클라이언트로 인구 데이터 시그널 전송 함수"""
        self.clientapp.send_realty_info_access(self.data)

    def infra_signal(self):
        """클라이언트로 인프라 데이터 시그널 전송 함수"""
        self.clientapp.send_infra_data_access(self.data)

    def store_signal(self):
        """클라이언트로 편의점 월 매출 평균 데이터 시그널 전송 함수"""
        self.clientapp.send_store_data_access(self.data)

    def result_signal(self):
        """클라이언트로 결과값 시그널 전송 함수"""
        self.clientapp.send_result_data_access(self.data)

    def show_population(self, year_):
        """유동인구 출력 함수"""
        # 맷플롯 캔버스 만들기 및 레이아웃에 캔버스 추가
        self.clear_layout(self.verticalLayout)
        canvas = FigureCanvas(plt.figure())
        self.verticalLayout.addWidget(canvas)
        self.create_population_plot(year_)

    def show_infra(self, infra_):
        """주변 인프라 출력 함수"""
        self.clear_layout(self.verticalLayout)
        canvas = FigureCanvas(plt.figure())
        self.verticalLayout.addWidget(canvas)

        # 샘플 차트 생성
        self.create_infra_plot(infra_)  # 파이 그래프

    def show_store(self, store_):
        """편의점 매출 출력 함수"""
        self.clear_layout(self.verticalLayout)
        store_data = self.decoder.binary_to_obj(store_)
        data_list = []
        self.num = store_data.bus_business_num
        data_list.append(self.num)
        sales = store_data.bus_sales
        data_list.append(sales)
        sales_num = store_data.bus_sales_num
        data_list.append(sales_num)
        canvas = StoreData(data_list, 1)
        self.verticalLayout.addWidget(canvas)

    def show_result(self, result_):
        """입지 결과 출력 함수"""
        self.clear_layout(self.verticalLayout)
        result_data = self.decoder.binary_to_obj(result_)
        cp1 = result_data.inf_cp1
        lf2 = result_data.inf_lf2
        sc3 = result_data.inf_sc3
        pk4 = result_data.inf_pk4
        su5 = result_data.inf_su5
        ct6 = result_data.inf_ct6
        ad7 = result_data.inf_ad7
        hc8 = result_data.inf_hc8
        bd9 = result_data.inf_bd9
        rf0 = result_data.inf_rf0
        data_list = []
        # 점수 계산
        total_score = 50 + (lf2 * 16) + (sc3 * 14) + (pk4 * 4) + (su5 * 6) + (ct6 * 18) + (ad7 * 20) + (hc8 * 4) + (bd9 * 10) + (rf0 * 8) - (cp1 * 4 + self.num)
        data_list.append(int(total_score))
        # 예측 창업 비용
        if self.data.rea_realty_ctg == '월세':
            total_low_cash = self.data.reg_deposit + 2200 + 3600
            total_high_cash = self.data.reg_deposit + 2200 + 5000
        elif self.data.rea_realty_ctg == '매매':
            total_low_cash = self.data.reg_selling_price + 2200 + 3600
            total_high_cash = self.data.reg_selling_price + 2200 + 5000
        data_list.append(total_low_cash)
        data_list.append(total_high_cash)
        canvas = StoreData(data_list, 2)
        self.verticalLayout.addWidget(canvas)

    def window_option(self):
        """프로그램 실행시 첫 화면 옵션 설정 함수"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.move(600, 241)
        self.back_btn_2.setChecked(True)
        self.label.setText(self.data.rea_rourist)


    def clear_layout(self, layout: QLayout):
        """레이아웃 안의 모든 객체를 지웁니다."""
        if layout is None or not layout.count():
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
            # 아이템이 레이아웃일 경우 재귀 호출로 레이아웃 내의 위젯 삭제
            else:
                self.clear_layout(item.layout())


