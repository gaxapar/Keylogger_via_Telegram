using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Mail;
namespace GUI
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            guna2TextBox1.Text = "Проверка наличия библиотек...";
          
           
            InstallLibraries();
            
            string originalScriptPath = "main_original.py";
            string pythonScriptPath = "main.py";

            if (!File.Exists(originalScriptPath) && File.Exists(pythonScriptPath))
            {
                try
                {
                  
                    File.Copy(pythonScriptPath, originalScriptPath);
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Ошибка при создании резервной копии оригинального скрипта: " + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }

           
            if (!IsPythonInstalled())
            {
                MessageBox.Show("Python не установлен. Установите Python перед использованием.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            else if (!IsPyInstallerInstalled())
            {
                MessageBox.Show("PyInstaller не установлен. Установите PyInstaller перед использованием.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

       
        private bool IsPythonInstalled()
        {
            try
            {
                Process process = Process.Start(new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = "--version",
                    RedirectStandardOutput = true,
                    CreateNoWindow = true,
                    UseShellExecute = false
                });

                process.WaitForExit();
                return process.ExitCode == 0;
            }
            catch
            {
                return false;
            }
        }

        private bool IsPyInstallerInstalled()
        {
            try
            {
                Process process = Process.Start(new ProcessStartInfo
                {
                    FileName = "pyinstaller",
                    Arguments = "--version",
                    RedirectStandardOutput = true,
                    CreateNoWindow = true,
                    UseShellExecute = false
                });

                process.WaitForExit();
                return process.ExitCode == 0;
            }
            catch
            {
                return false;
            }
        }

        private void btnBrowseIcon_Click(object sender, EventArgs e)
        {
            
            OpenFileDialog openFileDialog = new OpenFileDialog
            {
                Filter = "Icon Files (*.ico)|*.ico|All Files (*.*)|*.*",
                Title = "Выберите файл иконки"
            };
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                textBox3.Text = openFileDialog.FileName;
            }
        }

        private async void btnCompile_Click(object sender, EventArgs e)
        {
            string botToken = textBox1.Text;
            string userId = textBox2.Text;
            string iconPath = textBox3.Text;

            if (string.IsNullOrWhiteSpace(botToken) || string.IsNullOrWhiteSpace(userId))
            {
                MessageBox.Show("Пожалуйста, укажите оба значения: токен бота и ID пользователя.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                guna2WinProgressIndicator1.Visible = false;
                return;
            }

         
            string pythonScriptPath = "main.py";
            string scriptContent = File.ReadAllText(pythonScriptPath);

            scriptContent = ReplaceBotTokenAndUserId(scriptContent, botToken, userId);

        
            try
            {
                File.WriteAllText(pythonScriptPath, scriptContent);
                guna2WinProgressIndicator1.Visible = true;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при сохранении скрипта: " + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                guna2WinProgressIndicator1.Visible = false;
                return;
            }

           
            string pyInstallerArgs = "--onefile --noconsole " + pythonScriptPath;

            if (!string.IsNullOrEmpty(iconPath))
            {
                pyInstallerArgs += " --icon \"" + iconPath + "\"";
            }

            await CompileWithPyInstallerAsync(pyInstallerArgs);
        }

        private async Task CompileWithPyInstallerAsync(string pyInstallerArgs)
        {
            try
            {
             
                await Task.Run(() =>
                {
                    ProcessStartInfo startInfo = new ProcessStartInfo
                    {
                        FileName = "pyinstaller",
                        Arguments = pyInstallerArgs,
                        UseShellExecute = false,  
                        CreateNoWindow = true,   
                        RedirectStandardOutput = true, 
                        RedirectStandardError = true,   
                        StandardOutputEncoding = Encoding.UTF8, 
                        StandardErrorEncoding = Encoding.UTF8  
                    };

                    Process process = Process.Start(startInfo);

                    StringBuilder output = new StringBuilder();
                    StringBuilder error = new StringBuilder();

                   
                    Task.WhenAll(
                        Task.Run(() =>
                        {
                            string line;
                            while ((line = process.StandardOutput.ReadLine()) != null)
                            {
                                output.AppendLine(line);  
                                UpdateTextBox(output.ToString());  
                            }
                        }),
                        Task.Run(() =>
                        {
                            string line;
                            while ((line = process.StandardError.ReadLine()) != null)
                            {
                                error.AppendLine(line);  
                                UpdateTextBox(error.ToString());  
                            }
                        })
                    ).Wait();

                    process.WaitForExit();

                    
                    this.Invoke(new Action(() =>
                    {
                        if (process.ExitCode == 0)
                        {
                            MessageBox.Show("EXE файл был успешно создан!", "Успех", MessageBoxButtons.OK, MessageBoxIcon.Information);
                            guna2WinProgressIndicator1.Visible = false;

                         
                            string exeFolderPath = Path.Combine(Directory.GetCurrentDirectory(), "dist");
                            if (Directory.Exists(exeFolderPath))
                            {
                               
                                
                                Process.Start("explorer.exe", exeFolderPath);
                            }
                            else
                            {
                                MessageBox.Show("Папка с EXE файлом не найдена.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                            }
                        }
                        else
                        {
                            MessageBox.Show("Произошла ошибка в процессе компиляции.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                    }));
                });
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при выполнении PyInstaller: " + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

       
        private void UpdateTextBox(string text)
        {
            if (this.InvokeRequired)
            {
               
                this.Invoke(new Action<string>(UpdateTextBox), new object[] { text });
            }
            else
            {
              
                textBoxOutput.Text = text;
            }
        }

        private void btnReset_Click(object sender, EventArgs e)
        {
          
            string pythonScriptPath = "main.py";
            string originalScriptPath = "main_original.py";

            if (File.Exists(originalScriptPath))
            {
                try
                {
                    
                    File.Copy(originalScriptPath, pythonScriptPath, true);

                   
                    string scriptContent = File.ReadAllText(pythonScriptPath);
                    scriptContent = RestoreBotTokenAndUserId(scriptContent);

                    File.WriteAllText(pythonScriptPath, scriptContent);

                    MessageBox.Show("Скрипт был восстановлен до оригинальной версии с заглушками.", "Восстановление", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Ошибка при восстановлении скрипта: " + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            else
            {
                MessageBox.Show("Оригинальная версия скрипта не найдена.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void btnExit_Click(object sender, EventArgs e)
        {
           
            this.Close();
        }

        private string ReplaceBotTokenAndUserId(string scriptContent, string botToken, string userId)
        {
       
            scriptContent = scriptContent.Replace("BOT_TOKEN = \"<your_token_here>\"", "BOT_TOKEN = \"" + botToken + "\"");
            scriptContent = scriptContent.Replace("ALLOWED_USER_ID = <your_user_id_here>", "ALLOWED_USER_ID = " + userId);

            return scriptContent;
        }

        private string RestoreBotTokenAndUserId(string scriptContent)
        {
            scriptContent = scriptContent.Replace("BOT_TOKEN = \"" + GetBotTokenFromScript() + "\"", "BOT_TOKEN = \"<your_token_here>\"");
            scriptContent = scriptContent.Replace("ALLOWED_USER_ID = " + GetUserIdFromScript(), "ALLOWED_USER_ID = <your_user_id_here>");

            return scriptContent;
        }

        private string GetBotTokenFromScript()
        {
           
            string scriptContent = File.ReadAllText("main.py");
            var tokenStart = scriptContent.IndexOf("BOT_TOKEN = \"") + 13;
            var tokenEnd = scriptContent.IndexOf("\"", tokenStart);
            return scriptContent.Substring(tokenStart, tokenEnd - tokenStart);
        }

        private string GetUserIdFromScript()
        {
           
            string scriptContent = File.ReadAllText("main.py");
            var userIdStart = scriptContent.IndexOf("ALLOWED_USER_ID = ") + 18;
            var userIdEnd = scriptContent.IndexOf("\n", userIdStart);
            return scriptContent.Substring(userIdStart, userIdEnd - userIdStart);
        }

    
        private void guna2ImageButton1_Click(object sender, EventArgs e)
        {
            Process.Start("https://t.me/BotFather");
        }
        private async void InstallLibraries()
        {
           
            string[] requiredLibraries = new string[] { "python", "pyinstaller" };

           
            guna2TextBox1.AppendText("\nПроверка наличия библиотек...");
            guna2TextBox1.Refresh();  

           
            foreach (string library in requiredLibraries)
            {
               
                guna2TextBox1.AppendText("\nПроверка: " + library);
                guna2TextBox1.Refresh(); 

                if (!IsLibraryInstalled(library))
                {
                
                    guna2TextBox1.AppendText("\n" + library + " не установлен. Установка...");
                    guna2TextBox1.Refresh(); 

                   
                    await InstallLibraryAsync(library);
                }
                else
                {
                    
                    guna2TextBox1.AppendText("\n" + library + " уже установлен.");
                    guna2TextBox1.Refresh();  
                }
            }

          
            guna2TextBox1.AppendText("\nВсе библиотеки установлены и готовы к использованию.");
            guna2TextBox1.Refresh(); 
        }

       
        private bool IsLibraryInstalled(string library)
        {
            try
            {
                Process process = Process.Start(new ProcessStartInfo
                {
                    FileName = library,
                    Arguments = "--version",
                    RedirectStandardOutput = true,
                    CreateNoWindow = true,
                    UseShellExecute = false
                });

                process.WaitForExit();
                return process.ExitCode == 0;
            }
            catch
            {
                return false;
            }
        }

        private async Task InstallLibraryAsync(string library)
        {
            try
            {

                if (library == "python" || library == "pyinstaller")
                {
                    ProcessStartInfo startInfo = new ProcessStartInfo
                    {
                        FileName = "pip",
                        Arguments = (library == "python" ? "install python" : "install pyinstaller"),
                        RedirectStandardOutput = true,
                        CreateNoWindow = true,
                        UseShellExecute = false
                    };

                    Process process = Process.Start(startInfo);
                    process.WaitForExit();

                    if (process.ExitCode == 0)
                    {
                        guna2TextBox1.AppendText("\n" + library + " успешно установлен.");
                        guna2TextBox1.Refresh();  
                    }
                    else
                    {
                        guna2TextBox1.AppendText("\nОшибка при установке " + library + ".");
                        guna2TextBox1.Refresh();  
                    }
                }
            }
            catch (Exception ex)
            {
                guna2TextBox1.AppendText("\nОшибка при установке " + library + ": " + ex.Message);
                guna2TextBox1.Refresh(); 
            }
        }


        private void guna2ImageButton2_Click(object sender, EventArgs e)
        {
            Process.Start("https://t.me/user_irbot");
        }

        private void guna2ImageButton6_Click(object sender, EventArgs e)
        {
            Process.Start("https://t.me/psmib");
        }

        private void guna2HtmlLabel5_Click(object sender, EventArgs e)
        {

        }
    }
}
