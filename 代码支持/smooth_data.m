function [filtered_data, original_indices] = smooth_data(x,win_size,threshold)
% 初始化一个空数组来存储平滑后的数据
smoothed_data = zeros(1, length(x));

% 执行滑动平均
for i = 1:length(x)
    start_idx = max(1, i - floor(win_size/2));
    end_idx = min(length(x), i + floor(win_size/2));
    window_data = x(start_idx:end_idx);
    smoothed_data(i) = mean(window_data);
end
% 剔除异常值
% 计算数据的均值和标准差
    mean_value = mean(smoothed_data);
    std_deviation = std(smoothed_data);

    % 确定异常值的阈值
    outlier_threshold = mean_value + threshold * std_deviation;
    
    % 找到数据中大于阈值的异常值的索引
    outlier_indices = find(smoothed_data > outlier_threshold);

    % 剔除异常值
    filtered_data = smoothed_data;
    filtered_data(outlier_indices) = [];

    % 返回原始索引
    original_indices = 1:numel(smoothed_data);
    original_indices(outlier_indices) = [];