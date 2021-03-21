# 実証実験3手順
## 事前準備
1. カメラの事前準備
   1. 天井にカメラ2台を設置
   2. 座標の中心をマーキング
      1. window 1: `roslaunch rpl 0-1_centerImage.launch`
   3. 中心位置から半径1.5m(可能であれば2m)を50cm感覚でマーキング
   4. 中心位置にロボットの初期位置をマーキング(ロボットから見て右向き)
2. ロボットで地図を生成

## テストケース1:マーカ位置推定精度の検証
1. ロボットを各ポイントに移動させ、位置情報を保存
 - `roslaunch rpl 1-1_capture_position.launch`を起動
 - `rostopic pub /AR/create std_msgs/String "data: 'record'"`で画像と位置情報を保存
2. 床座標からfloor.csvと変換行列を作成
 - `python ./scripts/1-2_create_truevalue.py`を内部パラメータを変えて実行(floor.csvを出力)
 - `python ./scripts/1-3_create_transMatrix.py`を内部のパラメータを変えて実行(変換行列と比較結果のcsvを出力)
3. ※各位置情報をプロット、統計を取り信頼区間を導出

## テストケース2:※
1. ロボットを初期位置へ移動させ位置推定を開始
 - `roslaunch rpl estimate_position.launch`をパラメータを変えて起動
3. ロボットの移動履歴を保存
   1. rosbagを起動し、位置情報とコマンドのログを取得
       - `rosbag record /AR/integrated_pose /command/control /command/state /command/mission /cartographer/pose /RB/estimated_pose /RB/confution_pose /RB/confution_pose/position /RB/confution_pose/degree /AR/camera_pose /AR/estimated_pose /AR/create /map /points2`
   2. ロボットへWPを渡し、移動指示
       1. `rosrun rpl minimini2_command.py`をパラメータを変えて起動（WPと実行指示）
       2. `rostopic pub /command/control eams_msgs/Control "{header: auto, command: 1}"`
   3. ※マーカ座標とロボット座標を比較

## テストケース3:※
1. ローカル上で誤り検出
   1. ロボットを初期位置へ移動させ位置推定を開始
       - `roslaunch rpl estimate_position.launch`をパラメータを変えて起動
   2. rosbagを起動し、位置情報とコマンドのログを取得
       - `rosbag record /AR/integrated_pose /command/control /command/state /command/mission /cartographer/pose /RB/estimated_pose /RB/confution_pose /RB/confution_pose/position /RB/confution_pose/degree /AR/camera_pose /AR/estimated_pose /AR/create /map /points2`
   3. ローカル側で検出機能を実行
       - `roslaunch rpl 3-1_detect_error_position.launch`をパラメータを変えて起動
   4. ロボットの誤り生成プログラムを起動
       - X方向の誤り：`rosrun rpl error_pose_generator.py _direction:=x _value:=0.01`
       - Y方向の誤り：`rosrun rpl error_pose_generator.py _direction:=y _value:=0.1`
   5. ロボットのstateが停止に変化したことを確認
   6. 誤りを初期化
       - `rostopic pub /RB/confution_pose/position geometry_msgs/Point "{x: 0.0,y: 0.0,z: 0.0}"`
2. クラウド上で誤り検出
   1. ロボットを初期位置へ移動させ位置推定を開始
       - `roslaunch rpl estimate_position.launch`をパラメータを変えて起動
   2. rosbagを起動し、位置情報とコマンドのログを取得
       - `rosbag record /AR/integrated_pose /command/control /command/state /command/mission /cartographer/pose /RB/estimated_pose /RB/confution_pose /RB/confution_pose/position /RB/confution_pose/degree /AR/camera_pose /AR/estimated_pose /AR/create /map /points2`
   3. クラウド側で検出機能を実行
       - `roslaunch rpl 3-1_detect_error_position.launch`をパラメータを変えて起動
   4. ロボットの誤り生成プログラムを起動
       - X方向の誤り：`rosrun rpl error_pose_generator.py _direction:=x _value:=0.01`
       - Y方向の誤り：`rosrun rpl error_pose_generator.py _direction:=y _value:=0.1`
   5. ロボットのstateが停止に変化したことを確認
   6. 誤りを初期化
       - `rostopic pub /RB/confution_pose/position geometry_msgs/Point "{x: 0.0,y: 0.0,z: 0.0}"`

## demo
1. ロボットを初期位置へ移動させ位置推定を開始
   - `roslaunch rpl demo.launch`をパラメータを変えて起動
2. rvizを起動
3. 誤り検出及びアラートの起動
   - `roslaunch rpl detector_alert.launch`
4. ロボットへWPを渡し、移動指示
   1. `rosrun rpl minimini2_command.py`をパラメータを変えて起動（WPと実行指示）
   2. `rostopic pub /command/control eams_msgs/Control "{header: auto, command: 1}"`
5. ロボットの誤り生成プログラムを起動
   - X方向の誤り：`rosrun rpl error_pose_generator.py _direction:=x _value:=0.01`
   - Y方向の誤り：`rosrun rpl error_pose_generator.py _direction:=y _value:=0.1`
6. 誤りを初期化
   - `rostopic pub /RB/confution_pose/position geometry_msgs/Point "{x: 0.0,y: 0.0,z: 0.0}"`
