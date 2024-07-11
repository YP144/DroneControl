
% Panggilan fungsi dari dalam script
% hasil = fungsiDalamScript(5);
% disp(['Hasil dari fungsi dalam script adalah: ', num2str(hasil)]);
tz = 10;
t = 0:0.01:tz; % Rentang waktu simulasi
kec = 0.1;
y = sistemX("maju",0.1,2);
disp(y)

% initialY = 2;
% setPointY = 8;
% 
% Waktu simulasi
% dt = 0.01;  % Interval waktu
% t = 0:dt:10;
% 
% % Parameter PID
% Kp = 100;   % Gain proporsional
% Ki = 1;   % Gain integral
% Kd = 0.5; % Gain derivatif
% 
% % Inisialisasi variabel
% n = length(t);
% u = zeros(1, n);   % Sinyal kontrol
% y = zeros(1, n);   % Respons sistem
% e = zeros(1, n);   % Error
% integral = 0;      % Bagian integral
% previous_error = 0;  % Error sebelumnya
% 
% % Simulasi loop
% for i = 2:n
%     %calculate posisi sekarang
%     posisiNow = initialY
% 
%     % Hitung error
%     e(i) = setPointY - y(i-1);
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

























% Definisi fungsi dalam script
function y = sistemX(arah, kec, t)
    if arah == "maju"
        gainMaju = 937.34 * kec + 0.8953;
        tauMaju = 1.2396;
        s = tf('s'); % Definisikan operator Laplace
        Gmaju = gainMaju / (tauMaju * s + 1); % Fungsi transfer sistem
        U = 1 / s^2; % Fungsi transfer sinyal ramp
        Ymaju = Gmaju * U % Fungsi transfer output
        Ystep = s * Gmaju * U;
        % Simulasi dan Plot Respon
        outsim = step(Ystep, t); % Hitung respon terhadap sinyal ramp
        y = outsim(end);

    elseif arah == "mundur"
        gainMundur = -1*(1242.79 * kec - 4.531);
        tauMundur = 1.949;
        s = tf('s'); % Definisikan operator Laplace
        Gmundur = gainMundur / (tauMundur * s + 1); % Fungsi transfer sistem
        U = 1 / s^2; % Fungsi transfer sinyal ramp
        Ymundur = Gmundur * U % Fungsi transfer output
        Ystep = s * Gmundur * U;
        % Simulasi dan Plot Respon
        outsim = step(Ystep, t); % Hitung respon terhadap sinyal ramp
        y = outsim(end);
    end
end




