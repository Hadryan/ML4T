import talib 

periods_list = [2, 3, 4, 5, 10]

def cross_over(x, y, data):
    data[f'RSI_{x}-RSI_{y}'] = data[f'RSI_{x}'] - data[f'RSI_{y}']
    

def get_features(data):
    tech_data = pd.DataFrame(index=data.index);

    for t in periods_list:
        tech_data[f'SMA_{t}'] = talib.SMA(data.close,timeperiod=t)
        tech_data[f'MOM_{t}'] = talib.MOM(data.close, timeperiod=t)
        tech_data[f'RSI_{t}'] = talib.RSI(data.close, timeperiod=t)
        tech_data[f'MA_{t}'] = talib.MA(data.close, timeperiod=t)
        tech_data[f'DX_{t}'] = talib.DX(data.high, data.low, data.close, timeperiod=t)
        tech_data[f'volume_change_{t}'] = data.volume.pct_change(periods=t)
        tech_data[f'volatility_{t}'] = data.close.pct_change(periods=t).std()
        tech_data[f'ADX_{t}'] = talib.ADX(data.high, data.low, data.close, timeperiod=t)
        tech_data[f'ADXR_{t}'] = talib.ADXR(data.high, data.low, data.close, timeperiod=t)
        tech_data[f'AROONOSC_{t}'] = talib.AROONOSC(data.high, data.low, timeperiod=t)
        tech_data[f'ROC_{t}'] = talib.ROC(data.close, timeperiod=t)
        tech_data[f'BIAS_{t}'] = (data['close'] - data['close'].rolling(t, min_periods=1).mean())/ data['close'].rolling(t, min_periods=1).mean()*100
        tech_data[f'BOLL_upper_{t}'], tech_data[f'BOLL_middle_{t}'], tech_data[f'BOLL_lower_{t}'] = talib.BBANDS(
                data.close,
                timeperiod=t,
                nbdevup=2,
                nbdevdn=2,
                matype=0)

    tech_data['SAR'] = talib.SAR(data.high, data.low)
    tech_data['AD'] = talib.AD(data.high, data.low, data.close, data.volume)
    tech_data['OBV'] = talib.OBV(data.close, data.volume)
    tech_data['target'] = data.close.pct_change().shift(-1).apply(lambda x: 1 if x > 0 else -1).fillna(0)
    tech_data['time'] = data.time
    tech_data = tech_data.set_index('time')

    reduce(lambda x, y: cross_over(x, y, tech_data), periods_list)
    
    features = list(set(tech_data.columns) - set(data.columns) - set(['target'])) 
    return tech_data.dropna(), features


