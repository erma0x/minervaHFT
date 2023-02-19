from pykafka import KafkaClient
import pickle

# Creazione del cliente Kafka
client = KafkaClient(hosts="localhost:9092")

# Scelta dell'argomento (topic)
topic = client.topics['orderbook']

# Creazione del produttore
producer = topic.get_sync_producer()

# Creazione della lista
my_list = [1233423,[[2312,0],[2410,23]],[[123,4],[233,2]]]

NEW = [1673556769.721951,
 '[[18938.43, 0], [18938.44, 0], [18938.75, 0], [18938.77, 0], [18938.82, 0], [18938.88, 0], [18938.89, 0], [18938.92, 0], [18939.04, 0], [18939.06, 0], [18939.07, 0], [18939.08, 0], [18939.11, 0], [18939.12, 0], [18939.13, 0], [18939.15, 0], [18939.16, 0], [18939.17, 0], [18939.27, 0], [18939.28, 0], [18939.29, 0], [18939.3, 0], [18939.35, 0], [18939.37, 0], [18939.38, 0], [18939.4, 0], [18939.44, 0], [18939.48, 0], [18939.49, 0], [18939.59, 0], [18939.69, 0], [18939.75, 0], [18939.76, 0], [18939.77, 0], [18939.85, 0], [18939.94, 0], [18939.98, 0], [18940.01, 0], [18940.04, 0], [18940.05, 0], [18940.06, 0], [18940.07, 0], [18940.08, 0], [18940.09, 0], [18940.11, 0], [18940.12, 0], [18940.14, 0], [18940.18, 0], [18940.2, 0], [18940.22, 0], [18940.34, 0], [18940.36, 0], [18940.41, 0], [18940.44, 0], [18940.45, 0], [18940.46, 0], [18940.47, 0], [18940.49, 0], [18940.5, 0], [18940.56, 0], [18940.62, 0], [18940.63, 0], [18940.64, 0], [18940.65, 0], [18940.67, 0], [18940.68, 0], [18940.69, 0], [18940.7, 0], [18940.72, 0], [18940.75, 0], [18940.78, 0], [18940.79, 0], [18940.8, 0], [18940.83, 0], [18940.84, 0], [18940.85, 0], [18940.95, 0], [18940.96, 0], [18940.97, 0], [18940.98, 0], [18940.99, 0], [18941.01, 0], [18941.05, 0], [18941.07, 0.002], [18941.08, 0], [18941.09, 0.03302], [18941.1, 0], [18941.11, 0.02655], [18941.12, 0], [18941.13, 0], [18941.15, 0], [18941.27, 0.03733], [18941.28, 0.3571], [18941.29, 0], [18941.3, 0.01698], [18941.31, 0.004], [18941.32, 0], [18941.33, 0.03341], [18941.34, 0], [18941.35, 0], [18941.36, 0], [18941.38, 0.18847], [18941.39, 0], [18941.46, 0], [18941.47, 0], [18941.48, 0], [18941.5, 0.00645], [18941.51, 0], [18941.56, 0.02], [18941.57, 0], [18941.58, 0.3692], [18941.59, 0.20215], [18941.66, 0], [18941.77, 0], [18941.78, 0], [18941.79, 0], [18941.8, 0], [18941.88, 0], [18941.9, 0], [18941.91, 0.00633], [18941.99, 0], [18942, 0], [18942.05, 0], [18942.06, 0.00676], [18942.1, 0], [18942.11, 0], [18942.13, 0], [18942.15, 0], [18942.16, 0], [18942.17, 0], [18942.18, 0.46077], [18942.19, 0.47911], [18942.23, 0], [18942.24, 0], [18942.27, 0], [18942.29, 0.1763], [18942.3, 0.14176], [18942.31, 0], [18942.36, 0], [18942.39, 0.1], [18942.42, 0], [18942.43, 0], [18942.46, 0], [18942.48, 0], [18942.6, 0.0405], [18942.63, 0], [18942.65, 0.01118], [18942.83, 0], [18942.97, 0], [18943.01, 0.002], [18943.03, 0], [18943.04, 0], [18943.05, 0], [18943.07, 0.006], [18943.09, 0.08735], [18943.1, 0.58774], [18943.11, 0], [18943.18, 0.0035], [18943.22, 0], [18943.23, 0], [18943.3, 0.11655], [18943.31, 0.97312], [18943.41, 1.1746], [18943.47, 0.00128], [18943.51, 2.1335], [18943.52, 0.3], [18943.53, 0.52784], [18943.55, 0.90598], [18943.7, 0.00396], [18943.71, 0.98947], [18943.74, 0.38895], [18943.75, 0], [18943.8, 0], [18943.81, 1.13849], [18943.99, 0.1], [18944.02, 0], [18944.03, 0], [18944.05, 0], [18944.06, 0.02093], [18944.09, 0.02774], [18944.11, 0], [18944.15, 0.59174], [18944.17, 0.01], [18944.18, 0.64066], [18944.2, 1.47927], [18944.21, 0], [18944.3, 0], [18944.31, 0], [18944.32, 0.076], [18944.35, 0.023], [18944.41, 0], [18944.47, 0.04], [18944.51, 0], [18944.57, 1.05563], [18944.64, 0.01], [18944.95, 0.63344], [18945.19, 0], [18945.2, 0.10645], [18945.23, 0], [18945.28, 0.00097], [18945.43, 0], [18945.47, 0.00737], [18945.55, 0], [18945.56, 0.00672], [18945.61, 0.42131], [18945.62, 0.1], [18945.64, 0], [18945.67, 0], [18945.93, 0], [18946.02, 0], [18946.04, 1.01824], [18946.07, 0], [18946.08, 0], [18946.09, 0], [18946.21, 0], [18946.22, 0], [18946.23, 0], [18946.27, 0], [18946.32, 0.02], [18946.33, 0], [18946.34, 0], [18946.42, 0.08], [18946.48, 0.39592], [18946.59, 0], [18946.61, 0.16], [18946.62, 0.0148], [18946.69, 0], [18946.94, 0.00402], [18947.07, 0.09961], [18947.35, 0.0399], [18947.61, 0], [18947.77, 0.6495], [18947.78, 1.58318], [18948.05, 0.03], [18948.21, 0.00069], [18948.24, 0], [18948.25, 0], [18948.27, 0], [18948.32, 0.16297], [18948.54, 0], [18948.85, 0.003], [18949.27, 0.158], [18949.43, 0], [18949.59, 0], [18949.86, 0], [18951.09, 0.11932], [18951.33, 0], [18951.55, 0], [18951.68, 0], [18951.78, 0.75823], [18951.88, 0.00132], [18951.95, 0.03], [18952, 1.97298], [18952.47, 0.2], [18953.32, 0], [18953.49, 0], [18954.08, 0.004], [18956.38, 0], [18957.34, 0], [18957.37, 0.0226], [18957.4, 0], [18957.53, 0], [18957.95, 0.02], [18958.63, 0], [18959.49, 1.32574], [18959.86, 0], [18959.89, 0.03945], [18960.42, 0], [18960.71, 0.00164], [18960.83, 0.0457], [18961.34, 0.45706], [18962.19, 0.15583], [18964.29, 0], [18965.97, 0], [18967.81, 0.4], [18973.47, 0.05378], [18974.08, 0.0029], [18974.5, 2], [18976.36, 0], [18976.49, 0.03487], [18978.1, 0], [18978.24, 0], [18978.52, 0.00135], [18978.76, 0.3], [18979.15, 0.05293], [18979.57, 0.00053], [18980, 4.24861], [18980.15, 0.03002], [19005.83, 0.2], [19014.19, 0], [19016.31, 0.00669], [19049.1, 0.02145], [19055.04, 0], [19074.21, 2.24155], [19488.1, 0], [19489.72, 0.0336], [20020.08, 0.0005], [20163.26, 0.00081], [21411.39, 0.00047], [21735.39, 0.00139]]',
 '[[18940, 0], [18939.99, 0], [18939.98, 0.00245], [18939.97, 0.38699], [18939.96, 0], [18939.95, 0], [18939.94, 0], [18939.93, 0], [18939.92, 0], [18939.91, 0], [18939.84, 0], [18939.83, 0], [18939.82, 0], [18939.81, 0], [18939.77, 0], [18939.76, 0.0535], [18939.75, 0], [18939.74, 0.01022], [18939.73, 0.05], [18939.72, 0], [18939.66, 0], [18939.65, 0], [18939.64, 0], [18939.6, 0], [18939.59, 0], [18939.58, 0], [18939.57, 0], [18939.51, 0], [18939.5, 0], [18939.49, 0], [18939.48, 0], [18939.43, 0.00655], [18939.42, 0], [18939.41, 0], [18939.4, 0], [18939.36, 0.05385], [18939.35, 0.00987], [18939.34, 0], [18939.33, 0], [18939.32, 0.00198], [18939.31, 0.002], [18939.3, 0], [18939.29, 0], [18939.28, 0], [18939.24, 0], [18939.23, 0], [18939.22, 0], [18939.13, 0], [18939.12, 0], [18939.11, 0], [18939.03, 0], [18939.02, 0], [18939.01, 0], [18938.99, 0.00632], [18938.93, 0], [18938.92, 0], [18938.91, 0], [18938.85, 0.00539], [18938.83, 0], [18938.82, 0], [18938.81, 0], [18938.8, 0], [18938.79, 0], [18938.78, 0], [18938.77, 0.02198], [18938.75, 0], [18938.74, 0], [18938.73, 0], [18938.72, 0], [18938.71, 0], [18938.7, 0], [18938.62, 0], [18938.61, 0], [18938.6, 0], [18938.56, 0], [18938.54, 0], [18938.53, 0], [18938.52, 0], [18938.51, 0], [18938.5, 0.02539], [18938.49, 0], [18938.48, 0], [18938.46, 0], [18938.45, 0.02599], [18938.43, 0.00069], [18938.42, 0], [18938.41, 0], [18938.39, 0], [18938.38, 0], [18938.33, 0], [18938.27, 0.00561], [18938.24, 0], [18938.19, 0], [18938.18, 0], [18938.15, 0], [18938.14, 0], [18938.12, 0.02599], [18938.11, 0], [18938.1, 0], [18938.07, 0], [18938.04, 0], [18938.03, 0], [18938.02, 0], [18938.01, 0], [18938, 0.1076], [18937.99, 0], [18937.98, 0.0426], [18937.97, 0], [18937.96, 0], [18937.95, 0], [18937.94, 0.27182], [18937.93, 0.024], [18937.88, 0.00864], [18937.87, 0], [18937.85, 0], [18937.84, 0], [18937.83, 0], [18937.8, 0], [18937.79, 0], [18937.77, 0], [18937.74, 0], [18937.73, 0], [18937.72, 0], [18937.71, 0], [18937.68, 0], [18937.65, 0], [18937.64, 0], [18937.6, 0.157], [18937.59, 0.10559], [18937.57, 0.024], [18937.55, 0.01999], [18937.52, 0], [18937.51, 0], [18937.46, 0.321], [18937.45, 0.3168], [18937.44, 0.18002], [18937.43, 0], [18937.36, 0.28781], [18937.34, 0.00857], [18937.33, 0], [18937.3, 0], [18937.22, 0.1056], [18937.08, 0.0046], [18937.07, 0], [18937.06, 0], [18937, 0.06029], [18936.92, 0.15897], [18936.91, 0.19019], [18936.9, 0.47526], [18936.8, 0], [18936.62, 0.21119], [18936.56, 0.10559], [18936.54, 0], [18936.53, 0], [18936.5, 0.1062], [18936.46, 0.00636], [18936.38, 0.1056], [18936.37, 0.05563], [18936.36, 0.2849], [18936.33, 0], [18936.28, 0.09961], [18936.24, 0.39524], [18936.22, 0], [18936.21, 0.10559], [18936.18, 0.0029], [18936.16, 0.00096], [18936.12, 0], [18936.06, 0], [18936.04, 0.10561], [18936, 0.02915], [18935.93, 0], [18935.87, 0], [18935.81, 0], [18935.72, 0], [18935.71, 0], [18935.7, 0], [18935.69, 0], [18935.62, 0], [18935.61, 0.26695], [18935.59, 0.003], [18935.47, 0.10645], [18935.46, 0], [18935.45, 0.66739], [18935.41, 0], [18935.37, 0], [18935.35, 0], [18935.15, 0.0025], [18935.14, 0], [18934.99, 0.63345], [18934.98, 0.63416], [18934.97, 0], [18934.84, 0.04631], [18934.83, 0.00594], [18934.72, 0.53336], [18934.71, 0], [18934.7, 0.92562], [18934.55, 0.01545], [18934.44, 0], [18934.39, 0.09961], [18934.35, 0], [18934.13, 0], [18934.12, 0.042], [18934.05, 0], [18933.98, 0.01316], [18933.97, 0.4082], [18933.95, 0.64744], [18933.93, 1.80646], [18933.92, 0.0069], [18933.91, 0], [18933.86, 0], [18933.84, 0.72826], [18933.61, 0], [18933.6, 0], [18933.41, 0], [18933.24, 0.04491], [18933.12, 0], [18932.96, 0], [18932.74, 0.24658], [18932.62, 0], [18932.59, 0.002], [18932.34, 0.04926], [18932.22, 0], [18932.16, 0], [18932.06, 0.05], [18932.04, 0.38026], [18931.95, 0], [18931.92, 0.0396], [18931.8, 0], [18931.32, 0.08673], [18931.21, 0], [18931.05, 0.34134], [18931.02, 1.00007], [18930.92, 0.01045], [18930.86, 0.00775], [18930.81, 0.2], [18930.68, 0.0396], [18930.61, 0.521], [18930.56, 0], [18930.35, 0], [18930.28, 0.158], [18930.25, 0.0109], [18930.01, 0], [18929.21, 0], [18928.5, 0.00541], [18928.36, 0.08], [18927.61, 0.0622], [18927.5, 0.00061], [18927.46, 0], [18926.93, 0], [18925.01, 0.07743], [18924.85, 0], [18924.65, 0], [18923.72, 1.05959], [18923.49, 0], [18923.31, 0], [18922.97, 0.53031], [18921.65, 0.04109], [18921.51, 0], [18921.26, 0], [18920.3, 0.07472], [18919.3, 0], [18919.17, 0], [18911.56, 0.3], [18910.9, 0], [18902.99, 0.09961], [18902.8, 0], [18900.69, 0.00235], [18898.97, 0], [18890.47, 0.521], [18889.59, 0.1001], [18872.88, 0.2], [18867.77, 0.44035], [18798.29, 0], [18792.3, 0.02146], [18460, 0.23254], [18277.72, 0.01188], [18256.78, 0.03202], [17992.27, 0.00061], [17048, 0.1325], [16853.02, 0.04394], [16467.47, 0.22443], [15152.49, 0.03238], [15151.2, 0], [9469.99, 0.00126], [9468.98, 0], [9468.88, 1]]']

# Serializzazione della lista in bytes
my_list_bytes = pickle.dumps(NEW)

# Inviare il messaggio in bytes all'argomento (topic)
#producer.produce(bytes(str(NEW).encode('utf-8')))
producer.produce(bytearray(NEW))