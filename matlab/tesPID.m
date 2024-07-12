
% Panggilan fungsi dari dalam script
% hasil = fungsiDalamScript(5);
% disp(['Hasil dari fungsi dalam script adalah: ', num2str(hasil)]);
% tz = 10;
% t = 0:0.01:tz; % Rentang waktu simulasi
% kec = 0.1;
% y = sistemX("maju",0.1,0.01);
% disp(y)

initialY = 200;
setPointY = 450;

% Waktu simulasi
tz = 10;
dt = 0.01;  % Interval waktu
t = 0:dt:tz;

% Parameter PID
Kp = 5;   % Gain proporsional
Ki = 0;   % Gain integral
Kd = 1; % Gain derivatif

% Inisialisasi variabel
n = length(t);
u = zeros(1, n);   % Sinyal kontrol
e = zeros(1, n);   % Error
integral = 0;      % Bagian integral
previous_error = 0;  % Error sebelumnya
tfl = 0;
y=[initialY];
umin1 = 0;
x = [200];
sp = [setPointY];

% % Simulasi loop
for i = 2:length(t)
    % Hitung error
    error = setPointY - y(end);
    toleransi = 5;
    if error < toleransi && error >-toleransi
        e(i) = 0;
    else
        e(i) = error;
    end

    % Hitung bagian integral
    integral = integral + e(i) * dt;

    % Hitung bagian derivatif
    derivative = (e(i) - previous_error) / dt;

    % Hitung sinyal kontrol PID
    u(i) = Kp * e(i) + Ki * integral + Kd * derivative;
    if u(i) > 0.25
        u(i) = 0.25;
    elseif u(i) < -0.25
        u(i) = -0.25;
    end
    % update y sekarang
    if u(i) > 0
        arah = "maju";
    elseif u(i) < 0
        arah = "mundur";
    end

    if (u(i) ~= umin1)
        tfl = t(i-1);
        initialY = y(end);
        y = [y,initialY+sistemX(arah, u(i), t(i)-tfl)];
    elseif (u(i) == umin1)
        y = [y,initialY+sistemX(arah, u(i), t(i)-tfl)];
    end

    umin1 = u(i);
    x = [x,200];
    sp = [sp, setPointY];
    % Simpan error sebelumnya
    previous_error = e(i);
end

plot(t,y);
hold on
plot(t,sp)

% Impor gambar drone
[drone_icon, ~, alpha] = imread('quadrotor.png');

% Tentukan skala ukuran gambar (sesuaikan dengan ukuran yang diinginkan)
icon_size = 60; % Ukuran gambar dalam pixel

figure(2);

xlabel('Time');
ylabel('Position (x)');

% Loop untuk animasi
for i = 1:length(t)
    figure(2);
    plot(x(1:i), y(1:i), 'b', 'LineWidth', 2); % Plot data yang sudah diperbarui
    axis([0 400 0 500]); % Sesuaikan batas sumbu x dan y sesuai kebutuhan
    grid on;
    hold on;
    % plot(x(i), y(i), 'ro', 'MarkerSize', 10); % Plot titik posisi saat ini sebagai lingkaran merah
    % Tampilkan gambar drone sebagai simbol titik posisi saat ini
    h = image(x(i), y(i), drone_icon, 'XData', [x(i)-icon_size/2 x(i)+icon_size/2], 'YData', [y(i)-icon_size/2 y(i)+icon_size/2]);
    % Atur AlphaData untuk menetapkan transparansi
    set(h, 'AlphaData', alpha);
    hold off;
    pause(0.01); % Jeda antara setiap frame animasi
end

% Definisi fungsi dalam script
function y = sistemX(arah, kec, t)
    if arah == "maju"
        if kec ~= 0
            gainMaju = 937.34 * kec + 0.8953;
        elseif kec == 0
            gainMaju = 0;
        end
        tauMaju = 1.2396;
        s = tf('s'); % Definisikan operator Laplace
        Gmaju = gainMaju / (tauMaju * s + 1); % Fungsi transfer sistem
        U = 1 / s^2; % Fungsi transfer sinyal ramp
        Ymaju = Gmaju * U; % Fungsi transfer output
        Ystep = s * Gmaju * U;
        % Simulasi dan Plot Respon
        outsim = step(Ystep, t); % Hitung respon terhadap sinyal ramp
        y = outsim(end);

    elseif arah == "mundur"
        if kec ~= 0
            gainMundur = -1*(1242.79 * kec - 4.531);
        elseif kec == 0
            gainMundur = 0;
        end
        
        tauMundur = 1.949;
        s = tf('s'); % Definisikan operator Laplace
        Gmundur = gainMundur / (tauMundur * s + 1); % Fungsi transfer sistem
        U = 1 / s^2; % Fungsi transfer sinyal ramp
        Ymundur = Gmundur * U; % Fungsi transfer output
        Ystep = s * Gmundur * U;
        % Simulasi dan Plot Respon
        outsim = step(Ystep, t); % Hitung respon terhadap sinyal ramp
        y = outsim(end);
    end
end



