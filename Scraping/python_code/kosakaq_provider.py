# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 15:00:00 2022

@author: Yokohama National University, Kosaka Lab
"""

import requests
from qiskit.providers import ProviderV1 as Provider #抽象クラスのインポート
from qiskit.providers.exceptions import QiskitBackendNotFoundError #エラー用のクラスをインポート
from exceptions import KosakaQTokenError, KosakaQBackendJobIdError, KosakaQBackendFilterError #エラー用のクラス（自作）をインポート
from kosakaq_backend import KosakaQBackend 
from kosakaq_job import KosakaQJob
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

class KosakaQProvider(Provider): #抽象クラスからの継承としてproviderクラスを作る

    def __init__(self, access_token=None):#引数はself(必須)とtoken(認証が必要な場合)、ユーザーに自分でコピペしてもらう
        super().__init__() #ソースコードは（）空なので真似した
        self.access_token = access_token #トークン定義  
        self.name = 'kosakaq_provider' #nameという変数を右辺に初期化、このproviderクラスの名づけ
        self.url = 'http://192.168.1.82' #リンク変更可能
        self.wjson = '/api/backends.json' #jsonに何を入れてサーバーに送るか
        self.jobson = '/job/'
    
    
    def backends(self, name=None, **kwargs):#API(サーバー)に今使えるbackendを聞く(Rabiが使えるとかunicornが使えるとかをreturn[使えるもの]で教えてくれる)
        """指定したフィルタリングと合うバックエンドたちを返すメソッド
        引数:
            name (str): バックエンドの名前(Rabiやunicorn).
            **kwargs: フィルタリングに使用される辞書型
        戻り値:
            list[Backend]:　フィルタリング基準に合うバックエンドたちのリスト
        """
        self._backend = [] #availableなバックエンドクラスのbkednameを入れていくためのリスト
        res = requests.get(self.url + self.wjson, headers={"Authorization": "Token " + self.access_token})
        response = res.json() #[{'id': 1, 'bkedid': 0, 'bkedname': 'Rabi', 'bkedstatus': 'unavailable','detail': 'Authentication credentials were not provided',...}, {'id': 2, 'bkedid': 1, 'bkedname': 'Unicorn', 'bkedstatus': 'available'}]
        if 'detail' in response[0]: #トークンが違ったらdetailの辞書一つだけがresponseのリストに入っていることになる
            raise KosakaQTokenError('access_token was wrong') #トークン間違いを警告
        for i in range(len(response)):
            if response[i]['bkedstatus'] =='available':
                if name == None:
                    self._backend.append(KosakaQBackend(self, response[i]['bkedname'], self.url, response[i]['bkedversion'], response[i]['bkednqubits'], 4096, 1))
                elif name == response[i]['bkedname']:
                    self._backend.append(KosakaQBackend(self, response[i]['bkedname'], self.url, response[i]['bkedversion'], response[i]['bkednqubits'], 4096, 1))  
                else:
                    pass
        return self._backend#responseのstatusがavailableかつフィルタリングにあうバックエンドたちのバックエンドクラスのインスタンスリストを返す
 
    
    def get_backend(self, name=None, **kwargs): #ユーザーに"Rabi"などを引数として入れてもらう、もしbackendsメソッドのreturnにRabiがあればインスタンスを作れる
        """指定されたフィルタリングに合うバックエンドを一つだけ返す(一つ下のメソッドbackendsの一つ目を取り出す)
       引数:
           name (str): バックエンドの名前
           **kwargs: フィルタリングに使用される辞書型
       戻り値:
           Backend: 指定されたフィルタリングに合うバックエンド
       Raises:
           QiskitBackendNotFoundError: バックエンドが見つからなかった場合、もしくは複数のバックエンドがフィルタリングに合う場合、もしくは一つもフィルタリング条件に合わない場合
       """
        backends = self.backends(name, **kwargs) #backendsという変数にbackendsメソッドのreturnのリストを代入
        if len(backends) > 1:
            raise QiskitBackendNotFoundError('More than one backend matches criteria')
        if not backends:
            raise QiskitBackendNotFoundError('No backend matches criteria.')

        return backends[0]


    def retrieve_job(self, job_id: str):#jobidを文字列として代入してもらう（指定してもらう）,対応するJobを返す
        """このバックエンドに投入されたjobを一つだけ返す
        引数:
            job_id: 取得したいjobのID
        戻り値:
            与えられたIDのjob
        Raises:
            KosakaQBackendJobIdError: もしjobの取得に失敗した場合、ID間違いのせいにする
        """
        res = requests.get(self.url + self.jobson, headers={"Authorization": "Token " + self.access_token}, params={"jobid": job_id})
        response = res.json()#辞書型{bkedlist,jobist,qobjlist}
        print(response)
        if response['joblist'][0]['jobid'] == job_id:
            for i in range(len(response['bkedlist'])):
                if response['bkedlist'][i]['bkedid'] == response['joblist'][0]['bkedid']:
                    bkedname = response['bkedlist'][i]['bkedname']
            backend = KosakaQBackend(self, bkedname, self.url, response['bkedlist'][i]['bkedversion'], response['bkedlist'][i]['bkednqubits'], 4096, 1)  
            #量子レジスタqを生成する。
            q = QuantumRegister(1)
            #古典レジスタcを生成する
            c = ClassicalRegister(2)
            qc = QuantumCircuit(q, c)
            string = response['qobjlist'][0][0]['gates']
            gateslist = eval(string) #gatelist=["H","X"]
            for gate_name in gateslist:
                if gate_name == "I":
                    qc.i(q[0])
                elif gate_name == "X":
                    qc.x(q[0])
                elif gate_name == "Y":
                    qc.y(q[0])
                elif gate_name == "Z":
                    qc.z(q[0])
                elif gate_name == "H":
                    qc.h(q[0])
                elif gate_name == "S":
                    qc.s(q[0])
                elif gate_name == "SDG":
                    qc.sdg(q[0])
                elif gate_name == "SX":
                    qc.sx(q[0])
                elif gate_name == "SXDG":
                    qc.sxdg(q[0])
                else:
                    pass
                
            return KosakaQJob(backend, response['joblist'][0]['jobid'], self.access_token, qc)
        else:
            raise KosakaQBackendJobIdError('Job_id was wrong')
     

    def jobs(self,
            limit: int = 10,
            skip: int = 0,
            jobstatus = None,
            jobid = None,
            begtime = None,
            bkedid = None,
            fintime = None,
            job_num = None,
            note = None,
            posttime = None,
            qobjid = None,
            userid = None
    ): #list[KosakaQJob]を返す
        """このバックエンドに送信されたjobのうち指定したフィルタに合うものを取得して、返す
        引数:
            limit: 取得するjobの上限数
            skip: jobを飛ばしながら参照
            jobstatus: このステータスを持つjobのみを取得する。
                    指定方法の例 `status=JobStatus.RUNNING` or `status="RUNNING"`
                    or `status=["RUNNING", "ERROR"]`
            jobid: jobの名前でのフィルタリング用。 job名は部分的にマッチする、そして
                    `regular expressions(正規表現)
               <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions>`_
               が使われる。
            begtime: 指定された開始日（現地時間）でのフィルター用。これは作成日がこの指定した現地時間より後のjobを探すのに使われる。
            fintime: 指定された終了日（現地時間）でのフィルター用。 これは作成日がこの指定された現地時間よりも前に作られたjobを見つけるために使われる。
            job_num: jobの番号
            note: メモ
            posttime: 投稿時間
            qobjid: qobjのID
            userid: ユーザーID
  
        戻り値:
           条件に合うjobのリスト
        Raises:
           KosakaQBackendFilterError: キーワード値が認識されない場合 (でも、メソッド内で使われてない)
        """
        jobs_list = [] #返す用のリスト
        res = requests.get(self.url + self.jobson, headers={"Authorization": "Token " + self.access_token})
        response = res.json()#辞書型{bkedlist(ラビ、ユニコーン),jobist(jobnumがjobの数だけ),qobjlist(qobjnumがqobjの数だけ、ゲートもたくさん)}
        print(response)
        for i in range(len(response['joblist'])):
            if response['joblist'][i]['begtime'] == begtime or response['joblist'][i]['begtime'] == None :
                if response['joblist'][i]['bkedid'] == bkedid or response['joblist'][i]['bkedid'] == None:
                    if response['joblist'][i]['fintime'] == fintime or response['joblist'][i]['fintime'] == None:
                        if response['joblist'][i]['job_num'] == job_num or response['joblist'][i]['job_num'] == None:
                            if response['joblist'][i]['jobid'] == jobid or response['joblist'][i]['jobid'] == None:
                                if response['joblist'][i]['jobstatus'] == jobstatus or response['joblist'][i]['jobstatus'] == None:
                                    if response['joblist'][i]['note'] == note or response['joblist'][i]['note'] == None:
                                        if response['joblist'][i]['posttime'] == posttime or response['joblist'][i]['posttime'] == None:
                                            if response['joblist'][i]['qobjid'] == qobjid or response['joblist'][i]['qobjid'] == None:
                                                if response['joblist'][i]['userid'] == userid or response['joblist'][i]['userid'] == None:
                                                    bked_id = response['joblist'][i]['bkedid']#代入用bkedid
                                                    bked_posi =bked_id-1 #代入用バックエンド番号
                                                    backend = KosakaQBackend(self, response['bkedlist'][bked_posi]['bkedname'], self.url, response['bkedlist'][bked_posi]['bkedversion'], response['bkedlist'][bked_posi]['bkednqubits'], 4096, 1)
                                                    #量子レジスタqを生成する。
                                                    q = QuantumRegister(1)
                                                    #古典レジスタcを生成する
                                                    c = ClassicalRegister(2)
                                                    qc = QuantumCircuit(q, c)
                                                    string = response['qobjlist'][i]['gates']
                                                    gateslist = eval(string) #gatelist=["H","X"]
                                                    for gate_name in gateslist:
                                                        if gate_name == "I":
                                                            qc.i(q[0])
                                                        elif gate_name == "X":
                                                            qc.x(q[0])
                                                        elif gate_name == "Y":
                                                            qc.y(q[0])
                                                        elif gate_name == "Z":
                                                            qc.z(q[0])
                                                        elif gate_name == "H":
                                                            qc.h(q[0])
                                                        elif gate_name == "S":
                                                            qc.s(q[0])
                                                        elif gate_name == "SDG":
                                                            qc.sdg(q[0])
                                                        elif gate_name == "SX":
                                                            qc.sx(q[0])
                                                        elif gate_name == "SXDG":
                                                            qc.sxdg(q[0])
                                                        else:
                                                            pass
                                                    jobs_list.insert(i, KosakaQJob(backend, response['joblist'][i]['jobid'], self.access_token, qc))
        if len(jobs_list) == 0:
            raise KosakaQBackendFilterError('Filter was Error')
        return jobs_list
                
 
    def __eq__(self, other): #等号の定義
        """Equality comparison.
        By default, it is assumed that two `Providers` from the same class are
        equal. Subclassed providers can override this behavior.
        """
        return type(self).__name__ == type(other).__name__


