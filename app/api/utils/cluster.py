from app.api.service.BusinessService import BusinessService
businessService = BusinessService()

from sklearn.cluster import KMeans # 第三方算法库，暂用

# kmeans聚类
class kemans_cluster:
    def get_data(self,data):
        data = businessService.get_all_webbo_text()
        return data
    def run(self):
        x_train, x_test, y_train, y_test = self.data_priview()
        # 送入算法
        knn = KMeans(n_clusters=self.cluster_sum) # 创建一个KMeans算法实例，n_clusters为初始的中心数
        knn.fit(x_train, y_train) # 将测试集送入算法
        # print(knn.labels_)
        # 获取预测结果
        y_predict = knn.predict(x_test) 
        title = 'Kmeans聚类散点图('+str(self.cluster_sum)+'个中心)'
        print('Kmeans预测准确度:{}'.format(knn.score(x_test,y_test)))
        
        self.showScatter(x_test,y_predict,title)

    