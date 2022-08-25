function transformTimeBySystime(timeStr) { //将文本字符串 : "2021-1-1" 转化为系统日期字符串 : "t2021-0-1"
    timeStrList = timeStr.split('-')
    var year = Number(timeStrList[0]);
    var month = Number(timeStrList[1]) - 1;
    var day = Number(timeStrList[2]);
    return "t" + toString(year) + "-" + toString(month) + "-" + toString(day);
};

function getFirstDayByMonth(timeStr) { //获取给定月份的第一天
    timeStrList = timeStr.split('-')
    var year = Number(timeStrList[0]);
    var month = Number(timeStrList[1]);
    return toString(year) + "-" + toString(month) + "-" + "1";
}

function transformStrByTime(timeStr) { //将文本字符串类转化为时间类
    timeStrList = timeStr.split('-')
    var year = Number(timeStrList[0]);
    var month = Number(timeStrList[1]);
    var day = Number(timeStrList[2]);
    return date(year, month, day);
}

function getGlobalDateSelectTime(bar, flag) { //获取日期过滤组件的值
    var year;
    var month;
    var day;
    if (flag == 'start') {
        var TimFroBar = right(bar.firstDates[0], len(bar.firstDates[0]) - 1);
        var TimFroBarList = TimFroBar.split('-');
    } else if (flag == 'end') {
        var TimFroBar = right(bar.secondDates[0], len(bar.secondDates[0]) - 1);
        var TimFroBarList = TimFroBar.split('-');
    }
    year = Number(TimFroBarList[0]);
    month = Number(TimFroBarList[1]) + 1;
    day = Number(TimFroBarList[2]);
    TimFroBar = date(year, month, day);
    return TimFroBar
};

function getCurrentDateSourceTime(bar, flag) { //获取日期范围控件的值
    if (flag == 'start') {
        return bar.getSelectedObjects()[0];
    } else if (flag == 'end') {
        return bar.getSelectedObjects().slice(-1)[0];
    }
};

function switching(key) { //输入0的时候返回1，输入1的时候返回0
    return -key + 1;
};

function isOneMonth(startDay, endDay) { //判断日期范围控件所选区的时间段是否在同一个月份
    if (day(startDay) == 1) {
        if (year(startDay) == year(endDay) && month(startDay) == month(endDay)) {
            return true
        } else {
            return false
        }
    } else {
        return false
    }
};

//获取一些常量
//1、报告期间的天数，这个常数决定了图表展示内容的长度或者宽度
var CURRENT_DATE_LENGTH = days360(param["currentDateSourceByStart"], param["currentDateSourceByEnd"], null) + 1;
//2、报告期间内涉及到的消费类型，这个常数决定了图表展示内容的长度或者宽度
var TYPE_LENGTH = TypeLength.data;
//3、调取预测模型里面的参数
var TMP_BY_JSON = eval(TmpByJson.data)

//全局设置
ExpenditureTrendChart.hiddenTip = true
ExpenditureBudgetTrendsChart.hiddenTip = true

//更新UI尺寸
//1、ExpenditureTrendChart：
ExpenditureTrendChart.width = mina([CURRENT_DATE_LENGTH * 38, 912]);
ExpenditureTrendChart.x = 500 + (456 - ExpenditureTrendChart.width * 0.5);
//2、ExpenditureBudgetTrendsChart：
ExpenditureBudgetTrendsChart.width = mina([CURRENT_DATE_LENGTH * 38, 912]);
ExpenditureBudgetTrendsChart.x = 500 + (456 - ExpenditureBudgetTrendsChart.width * 0.5);
//3、SpendingBoxFigure：
//SpendingBoxFigure.width = mina([TYPE_LENGTH * 80, 912]);
//SpendingBoxFigure.x = 500 + (456 - SpendingBoxFigure.width * 0.5);
//4、ExpenditureCompositionTable：
//ExpenditureCompositionTable.height = mina([TYPE_LENGTH * 60 + 30, 345]);
//ExpenditureCompositionTable.y = 442 - ExpenditureCompositionTable.height * 0.5;

//定义左上角时间控件的值
var currentDate = now();
globalDateNow.data = '当前日期：' + formatDate(currentDate, "yyyy年MM月dd日 HH点mm分");

//定义报告期间的起始和结束日期
var theDayofToday = today();
globalDataSelect.firstDates = [transformTimeBySystime(getFirstDayByMonth(formatDate(theDayofToday, 'yyyy-MM-dd')))]; //起始日期
globalDataSelect.secondDates = [transformTimeBySystime(formatDate(theDayofToday, 'yyyy-MM-dd'))]; //最终日期;

//获取报告期间的起始和结束时间
param["globalDataSelectByfirst"] = getGlobalDateSelectTime(globalDataSelect, 'start');
param["globalDataSelectBySecond"] = getGlobalDateSelectTime(globalDataSelect, 'end');

//让currentDateSource控件包含最小值
currentDateSource.includeMin = true;

//获取currentDateSource控件选择的最小值和最大值
param["currentDateSourceByStart"] = getCurrentDateSourceTime(currentDateSource, 'start');
param["currentDateSourceByEnd"] = getCurrentDateSourceTime(currentDateSource, 'end');

//这段暂时没用
var imageKey = 0;
currentDateSourceMode.image = '家庭账本/mode' + imageKey + '.png';
currentDateSourceModeLab.data = '吼';

//将报告期间天数赋值给文本框
daysNumber.data = CURRENT_DATE_LENGTH;

//预测模块
if (isOneMonth(param["currentDateSourceByStart"], param["currentDateSourceByEnd"]) == true) {
    MonthlyExpenditureForecast.visible = true;
    MonthlyExpenditureForecastLab.visible = true;
    if (CURRENT_DATE_LENGTH <= 23) {
        //根据多元回归预测月度花销（1-23天使用多元回归）
        var ExpenditureTrendData = getData("ExpenditureTrendChart", DATA);
        var subtotals = 0;
        var constant = TMP_BY_JSON[CURRENT_DATE_LENGTH - 1]["b"];
        for (i = 1; i <= CURRENT_DATE_LENGTH; i++) {
            subtotals = subtotals + ExpenditureTrendData.get(i, 1) * TMP_BY_JSON[CURRENT_DATE_LENGTH - 1]['x' + i];
        };
        MonthlyExpenditureForecast.data = subtotals + constant;
    } else {
        //根据累计均值回归预测月度花销（超过23天使用累计均值回归）
        MonthlyExpenditureForecast.data = AveAmountByEveryDay.data * day(eomonth(param["currentDateSourceByStart"], 0))
    }
} else {
    MonthlyExpenditureForecast.visible = false;
    MonthlyExpenditureForecastLab.visible = false;
};