% 
% Definisikan Parameter Sistem
kec = 0.1;
K = -1*(1242.79 * kec - 4.531);
tau = 1.949;
A = 1; % Kemiringan sinyal ramp

% Definisikan Sistem di Domain Laplace
s = tf('s'); % Definisikan operator Laplace
G = K / (tau * s + 1); % Fungsi transfer sistem

% Definisikan Sinyal Ramp
U = A / s^2; % Fungsi transfer sinyal ramp

% Hitung Respon Sistem
Y = G * U; % Fungsi transfer output
Ystep = s * G * U;
figure();

% Delay dan batas xlim
td = 0;
tz = 5;
t2 = 0:0.01:td; % Rentang waktu simulasi
y2 =[];
for i = 1:length(t2)
    y2 = [y2,0];
end

% Simulasi dan Plot Respon
t = 0:0.01:tz; % Rentang waktu simulasi
y = step(Ystep, t+td); % Hitung respon terhadap sinyal ramp

% Plot hasil simulasi
t4 = [t2,t];
tfinal = t4.';

y3 = y.';
y4 = [y2,y3];
yfinal = y4.';

plot(tfinal,yfinal);
title('Respon Sistem Orde 1 terhadap Sinyal Ramp');
xlabel('Waktu (detik)');
ylabel('Output y(t)');
grid on;
% % pidTuner(sys)

% % Definisikan parameter sistem
% K = 1;    % Gain
% tau = 1;  % Konstanta waktu
% 
% % Transfer function sistem
% num = K;            % Pembilang
% den = [tau 1];      % Penyebut
% sys = tf(num, den);
% 
% % Parameter PID
% Kp = 100;   % Gain proporsional
% Ki = 1;   % Gain integral
% Kd = 0.5; % Gain derivatif
% 
% % Waktu simulasi
% dt = 0.01;  % Interval waktu
% t = 0:dt:10;
% 
% % Input ramp
% setpoint = t;
% 
% % Inisialisasi variabel
% n = length(t);
% u = zeros(1, n);   % Sinyal kontrol
% y = zeros(1, n);   % Respons sistem
% e = zeros(1, n);   % Error
% integral = 0;      % Bagian integral
% previous_error = 0;  % Error sebelumnya
% 
% % Fungsi transfer sistem dalam bentuk state-space
% [A, B, C, D] = tf2ss(num, den);
% x = zeros(length(A), 1);  % Inisialisasi kondisi awal state
% 
% % Simulasi loop
% for i = 2:n
%     % Hitung error
%     e(i) = setpoint(i) - y(i-1);
% 
%     % Hitung bagian integral
%     integral = integral + e(i) * dt;
% 
%     % Hitung bagian derivatif
%     derivative = (e(i) - previous_error) / dt;
% 
%     % Hitung sinyal kontrol PID
%     u(i) = Kp * e(i) + Ki * integral + Kd * derivative;
% 
%     % Update kondisi state menggunakan persamaan state-space
%     x = x + dt * (A * x + B * u(i));
%     y(i) = C * x + D * u(i);
% 
%     % Simpan error sebelumnya
%     previous_error = e(i);
% end
% 
% % Plot hasil simulasi
% figure;
% plot(t, y, 'LineWidth', 2);
% hold on;
% plot(t, setpoint, 'r--', 'LineWidth', 1.5);
% grid on;
% xlabel('Waktu (detik)');
% ylabel('Amplitudo');
% title('Respons Sistem dengan Pengontrol PID terhadap Input Ramp');
% legend('Output', 'Setpoint');
