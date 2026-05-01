import pandas as pd

def apply_strategies(df):
    # 確保資料為數值格式 (若有文字請先轉為 float)
    cols = ['vol_trend', 'close_price', 'volume', 'ma5', 'ma10', 'k_val', 'd_val']
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 邏輯條件定義
    common_cond = (df['vol_trend'] > 1.86) & (df['volume'] > 3000)
    
    # 策略 1：當沖 (反彈低接)
    # 條件：F < J, J > L, R < 70, T > R
    intraday_cond = common_cond & (df['close_price'] < df['ma5']) & \
                    (df['ma5'] > df['ma10']) & (df['k_val'] < 70) & (df['d_val'] > df['k_val'])
    
    # 策略 2：波段 (多頭洗盤)
    # 條件：F >= J, J > L, R >= 70, T <= R
    swing_cond = common_cond & (df['close_price'] >= df['ma5']) & \
                 (df['ma5'] > df['ma10']) & (df['k_val'] >= 70) & (df['d_val'] <= df['k_val'])
    
    # 標記結果
    df['策略_當沖'] = intraday_cond
    df['策略_波段'] = swing_cond
    
    return df

# 讀取並執行
# 假設 df 是合併後的總表
# processed_df = apply_strategies(your_combined_df)
# result_intraday = processed_df[processed_df['策略_當沖'] == True]
# result_swing = processed_df[processed_df['策略_波段'] == True]