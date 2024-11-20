import React, { useState, useEffect } from 'react';
import { Upload, FileText, Database, Search, Download, Sparkles, ArrowRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/AIDataAssistant/card';
import { Alert, AlertDescription } from '@/components/AIDataAssistant/alert';

const AIDataAssistant = () => {
  const [uploadType, setUploadType] = useState('csv');
  const [file, setFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [success, setSuccess] = useState(false);
  const [activeStep, setActiveStep] = useState(1);
  const [isHovering, setIsHovering] = useState(false);

  // Animated background gradient with pulse effect
  useEffect(() => {
    const interval = setInterval(() => {
      const gradient = document.querySelector('.animated-gradient');
      if (gradient) {
        gradient.style.backgroundPosition = `${Date.now() / 30}px`;
      }
    }, 30);
    return () => clearInterval(interval);
  }, []);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsHovering(true);
  };

  const handleDragLeave = () => {
    setIsHovering(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsHovering(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile?.type === 'text/csv') {
      setFile(droppedFile);
      setSuccess(true);
      setActiveStep(2);
    }
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile?.type === 'text/csv') {
      setFile(selectedFile);
      setSuccess(true);
      setActiveStep(2);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-8 text-white relative overflow-hidden">
      {/* Animated background elements */}
      <div className="animated-gradient fixed top-0 left-0 w-full h-3 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(66,138,248,0.05),transparent_50%)] animate-pulse" />
      
      <div className="max-w-5xl mx-auto relative">
        <div className="flex items-center gap-4 mb-12 animate-fade-in">
          <div className="p-3 rounded-2xl bg-blue-500/20 backdrop-blur-lg rotate-3 hover:rotate-0 transition-transform duration-300">
            <Sparkles className="w-8 h-8 text-blue-400 animate-pulse" />
          </div>
          <h1 className="text-6xl font-bold bg-gradient-to-br from-white via-blue-400 to-purple-400 bg-clip-text text-transparent hover:scale-105 transition-transform duration-300">
            AI Data Assistant
          </h1>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-8">
          {[1, 2, 3].map((step) => (
            <div
              key={step}
              className={`flex items-center gap-3 p-4 rounded-xl transition-all duration-500 transform hover:scale-105 ${
                activeStep === step
                  ? 'bg-blue-500/20 border border-blue-400/30 shadow-lg shadow-blue-500/20'
                  : 'bg-gray-800/50 border border-gray-700'
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors duration-300 ${
                  activeStep === step ? 'bg-blue-500 text-white animate-pulse' : 'bg-gray-700 text-gray-400'
                }`}
              >
                {step}
              </div>
              <span className={`transition-colors duration-300 ${activeStep === step ? 'text-blue-400' : 'text-gray-400'}`}>
                {step === 1 ? 'Upload Data' : step === 2 ? 'Configure' : 'Results'}
              </span>
            </div>
          ))}
        </div>

        <Card className="bg-gray-800/50 border-gray-700 backdrop-blur-lg mb-8 overflow-hidden hover:shadow-xl transition-shadow duration-300">
          <CardHeader>
            <CardTitle className="text-2xl text-gray-200 flex items-center gap-2">
              <FileText className="w-6 h-6 text-blue-400 animate-bounce" />
              Select Data Source
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              <div className="flex gap-4">
                {['csv', 'sheets'].map((type) => (
                  <button
                    key={type}
                    onClick={() => setUploadType(type)}
                    className={`flex-1 p-6 rounded-xl border-2 transition-all duration-300 transform hover:scale-105 ${
                      uploadType === type
                        ? 'border-blue-400 bg-blue-500/10 shadow-lg shadow-blue-500/20'
                        : 'border-gray-700 hover:border-gray-600 bg-gray-800/50'
                    }`}
                  >
                    <div className="flex items-center justify-center gap-3">
                      {type === 'csv' ? (
                        <FileText className={`w-5 h-5 ${uploadType === type ? 'text-blue-400' : 'text-gray-400'}`} />
                      ) : (
                        <Database className={`w-5 h-5 ${uploadType === type ? 'text-blue-400' : 'text-gray-400'}`} />
                      )}
                      <span className={`font-medium ${uploadType === type ? 'text-blue-400' : 'text-gray-400'}`}>
                        {type === 'csv' ? 'CSV Upload' : 'Google Sheets'}
                      </span>
                    </div>
                  </button>
                ))}
              </div>

              {uploadType === 'csv' ? (
                <div
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  className={`border-2 border-dashed rounded-xl p-12 text-center transition-all duration-300 cursor-pointer transform hover:scale-102 ${
                    isHovering
                      ? 'border-blue-400 bg-blue-500/10 shadow-lg shadow-blue-500/20'
                      : 'border-gray-700 hover:border-gray-600'
                  }`}
                >
                  <input
                    type="file"
                    accept=".csv"
                    onChange={handleFileSelect}
                    className="hidden"
                    id="file-upload"
                  />
                  <label htmlFor="file-upload" className="cursor-pointer">
                    <div className={`transition-transform duration-300 ${isHovering ? 'scale-110' : 'scale-100'}`}>
                      <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4 animate-bounce" />
                      <p className="text-xl font-medium text-gray-200 mb-2">
                        Drop your CSV file here
                      </p>
                      <p className="text-sm text-gray-400 mb-4">or click to browse</p>
                      <p className="text-xs text-gray-500">Limit 200MB per file • CSV</p>
                    </div>
                  </label>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="relative group">
                    <input
                      type="text"
                      placeholder="Enter Google Sheet URL"
                      className="w-full p-4 bg-gray-900/50 border border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-200 pr-36 transition-all duration-300 group-hover:border-gray-600"
                    />
                    <button className="absolute right-2 top-2 bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-all duration-300 flex items-center gap-2 group">
                      Connect
                      <ArrowRight className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
                    </button>
                  </div>
                </div>
              )}

              {success && (
                <Alert className="bg-green-500/10 border-green-500/30 animate-fade-in">
                  <AlertDescription className="text-green-400 flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                    Data loaded successfully!
                  </AlertDescription>
                </Alert>
              )}
            </div>
          </CardContent>
        </Card>

        {success && (
          <>
            <Card className="bg-gray-800/50 border-gray-700 backdrop-blur-lg mb-8 animate-slide-up">
              <CardHeader>
                <CardTitle className="text-2xl text-gray-200 flex items-center gap-2">
                  <Search className="w-6 h-6 text-blue-400" />
                  Configure Analysis
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div className="group">
                    <label className="block text-sm font-medium text-gray-300 mb-2 group-hover:text-blue-400 transition-colors">
                      Select the main column for analysis
                    </label>
                    <select className="w-full p-4 bg-gray-900/50 border border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-200 transition-all duration-300 hover:border-gray-600">
                      <option>Select column...</option>
                      <option>Name</option>
                      <option>Company</option>
                      <option>Website</option>
                    </select>
                  </div>

                  <div className="group">
                    <label className="block text-sm font-medium text-gray-300 mb-2 group-hover:text-blue-400 transition-colors">
                      Enter your analysis prompt
                    </label>
                    <textarea
                      className="w-full p-4 bg-gray-900/50 border border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-200 min-h-32 transition-all duration-300 hover:border-gray-600"
                      placeholder="Get me the email address of {entity}"
                    ></textarea>
                  </div>

                  <button
                    onClick={() => {
                      setIsProcessing(true);
                      setActiveStep(3);
                    }}
                    className="w-full bg-blue-500 text-white py-4 rounded-xl hover:bg-blue-600 transition-all duration-300 flex items-center justify-center gap-2 group transform hover:scale-105"
                  >
                    <span>Start Analysis</span>
                    <ArrowRight className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
                    {isProcessing && (
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin ml-2"></div>
                    )}
                  </button>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gray-800/50 border-gray-700 backdrop-blur-lg animate-slide-up">
              <CardHeader>
                <CardTitle className="text-2xl text-gray-200 flex items-center gap-2">
                  <Download className="w-6 h-6 text-blue-400" />
                  Analysis Results
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div className="overflow-hidden rounded-xl border border-gray-700 transition-all duration-300 hover:border-gray-600">
                    <table className="min-w-full divide-y divide-gray-700">
                      <thead className="bg-gray-900/50">
                        <tr>
                          <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            Entity
                          </th>
                          <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            Extracted Information
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-gray-800/30 divide-y divide-gray-700">
                        <tr className="hover:bg-gray-700/30 transition-colors duration-200">
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                            Example Corp
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">
                            contact@example.com
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                  <div className="flex gap-4">
                    <button className="flex-1 bg-blue-500 text-white py-4 rounded-xl hover:bg-blue-600 transition-all duration-300 flex items-center justify-center gap-2 group transform hover:scale-105">
                      <Download className="w-4 h-4" />
                      <span>Download CSV</span>
                      <ArrowRight className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
                    </button>
                    {uploadType === 'sheets' && (
                      <button className="flex-1 bg-green-500 text-white py-4 rounded-xl hover:bg-green-600 transition-all duration-300 flex items-center justify-center gap-2 group transform hover:scale-105">
                        <Database className="w-4 h-4" />
                        <span>Update Sheet</span>
                        <ArrowRight className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
                      </button>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          </>
        )}
      </div>
    </div>
  );
};

export default AIDataAssistant;