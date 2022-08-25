format bank

% 获取多元回归模型的所有参数
b = ones(30, 1);

for i = 1:30
    b(1:i + 1, i + 1) = funcx(i, X, Y);
end

b(:, 1) = [];
% \\\\\\\\\\\\\\\\\\\\\\\\

% 多元线性回归与累计均值回归对于未来花销总预测模型的准确性对比
Predicted_BY_MLR = ones(55, 1);
Predicted_BY_MR = ones(55, 1);

for i = 1:30
    Predicted_BY_MLR(:, i + 1) = MLR(X(:, 1:i), b);
    Predicted_BY_MR(:, i + 1) = MR(X(:, 1:i), 30);
end

Predicted_BY_MLR(:, 1) = [];
Predicted_BY_MR(:, 1) = [];
Correlation_By_MLR = ones(1, 30);
Correlation_By_MR = ones(1, 30);

for i = 1:30
    Cov_By_MLR = cov(Predicted_BY_MLR(:, i), Y);
    Cov_By_MR = cov(Predicted_BY_MR(:, i), Y);
    Correlation_By_MLR(i) = Cov_By_MLR(1, 2) / sqrt(Cov_By_MLR(1, 1) * Cov_By_MLR(2, 2));
    Correlation_By_MR(i) = Cov_By_MR(1, 2) / sqrt(Cov_By_MR(1, 1) * Cov_By_MR(2, 2));
end

% 绘图
x1_lab = 1:30;
x2_lab = 1:30;
plot(x1_lab, Correlation_By_MLR, '+', Color = 'red'), hold on, plot(x2_lab, Correlation_By_MR, '*', Color = 'blue')
% \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

% 构建多元线性回归函数
function result = MLR(a, b)
    [~, LENGTH] = size(a);
    result = a * b(2:1 + LENGTH, LENGTH) + b(1, LENGTH);
end

% \\\\\\\\\\\\\\\\\\

% 构建累计均值回归函数
function result = MR(a, b)
    [~, LENGTH] = size(a);

    if LENGTH == 1
        result = (a / LENGTH) * b;
    else
        result = transpose((sum(transpose(a)) / LENGTH) * b);
    end

end

% \\\\\\\\\\\\\\\\\
% 构建多元回归模型获取参数
function result = funcx(LENGTH, X, Y)
    x_zscore = filloutliers(X, 'clip', 'mean'); % 离群值清洗，以均值的三倍为离群值，将离群值替换为均值
    % -- 在先期实验中，已通过对30个自变量与因变量共3288条数据的模拟，确定了不同参数对应的绝对值累计误差：
    % 'clip'       'mean'         98,674
    % 'center'     'mean'         286,966
    % 'clip'       'quartiles'    637,770
    % 'center'     'quartiles'    695,930
    % 'clip'       'median'       945,326
    % 'center'     'median'       1,358,290
    % 所以可得最好的离群值处理办法为'clip'，'mean'组合
    [m, ~] = size(X);
    %     for i = 1:LENGTH
    %         subplot(5, 6, i), plot(x_zscore(:, i), Y, '+'), xlabel(i)
    %     end
    x = [ones(m, 1), x_zscore(:, 1:LENGTH)];
    y = Y;
    [b, ~, ~, ~, ~] = regress(y, x);
    result = b;
end

% \\\\\\\\\\\\\\\\\\\\
