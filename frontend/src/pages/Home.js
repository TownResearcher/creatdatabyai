import React, { useState } from 'react';
import { Upload, Button, Progress, Card, message, Space, Typography } from 'antd';
import { InboxOutlined, DownloadOutlined } from '@ant-design/icons';
import { useSocket } from '../services/socket';
import { convertNovel } from '../services/api';

const { Dragger } = Upload;
const { Title, Text } = Typography;

const Home = () => {
  const [processing, setProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const socket = useSocket();

  const handleUpload = async (file) => {
    try {
      setProcessing(true);
      setProgress(0);
      
      // 监听处理进度
      socket.on('progress', (data) => {
        setProgress(data.percent);
      });

      // 上传并处理文件
      const response = await convertNovel(file);
      setResult(response.data);
      message.success('处理完成！');
    } catch (error) {
      message.error('处理失败：' + error.message);
    } finally {
      setProcessing(false);
    }
  };

  const downloadResult = () => {
    if (result) {
      const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'dataset.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  return (
    <div style={{ padding: '24px', maxWidth: '800px', margin: '0 auto' }}>
      <Title level={2}>小说转数据集工具</Title>
      
      <Card style={{ marginBottom: '24px' }}>
        <Dragger
          name="file"
          multiple={false}
          accept=".txt,.epub,.pdf"
          beforeUpload={(file) => {
            handleUpload(file);
            return false;
          }}
          disabled={processing}
        >
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">点击或拖拽文件到此处上传</p>
          <p className="ant-upload-hint">
            支持单个文件上传，文件格式：txt, epub, pdf
          </p>
        </Dragger>
      </Card>

      {processing && (
        <Card>
          <Space direction="vertical" style={{ width: '100%' }}>
            <Text>处理进度</Text>
            <Progress percent={progress} status="active" />
          </Space>
        </Card>
      )}

      {result && (
        <Card>
          <Space direction="vertical" style={{ width: '100%' }}>
            <Text>处理结果</Text>
            <pre style={{ 
              maxHeight: '300px', 
              overflow: 'auto',
              backgroundColor: '#f5f5f5',
              padding: '16px',
              borderRadius: '4px'
            }}>
              {JSON.stringify(result, null, 2)}
            </pre>
            <Button 
              type="primary" 
              icon={<DownloadOutlined />}
              onClick={downloadResult}
            >
              下载数据集
            </Button>
          </Space>
        </Card>
      )}
    </div>
  );
};

export default Home; 