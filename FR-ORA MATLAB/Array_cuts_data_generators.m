% Close the previous figures
close all;

% Operating frequnecy
FC = 433e6;

% Speed of light
C = physconst('LightSpeed');

% Element spacing
element_spacing = 0.1419;

cst_export_array_filepath = './ORA_433MHz_Far_field_best_edited.xlsx';

[gain, phi,theta] = customAntennaCSVImport(cst_export_array_filepath);

[pattern_phitheta,gain, phi,theta] = customPatternImport(cst_export_array_filepath);


[pattern_azel,az,el] = phitheta2azelpat(pattern_phitheta.', theta, phi);

ora_element = phased.CustomAntennaElement('AzimuthAngles',az,...
                          'ElevationAngles',el,...
                          'MagnitudePattern',pattern_azel,...
                          'PhasePattern',zeros(size(pattern_azel)));
                      

% Creating Uniform Linear Array cuts using the FR-ORA element

for i = 2:10
    n_elements = i;
    ula = phased.ULA('Element',ora_element, 'NumElements', n_elements,... 
    'ElementSpacing', element_spacing);
    azimuth_dbi = patternAzimuth(ula,FC,'PropagationSpeed',C);
    azimuth_slice = [az.' azimuth_dbi];
    elevation_dbi = patternElevation(ula,FC,'PropagationSpeed',C);
    elevation_slice = [az.' elevation_dbi];
    filename_az = sprintf('%d_%d_ora_uniform_az_slice.csv',1,i);
    filename_el = sprintf('%d_%d_ora_uniform_el_slice.csv',1,i);
    csvwrite(filename_az, azimuth_slice);
    csvwrite(filename_el, elevation_slice);
end

% Creating Uniform Rectangular Array cuts using the FR-ORA element

for j = 2:10
    for k = 2:10
        n_side_1 = j;
        n_side_2 = k;
        ura = phased.URA('Element', ora_element,'Size',[n_side_1 n_side_2],...
        'ElementSpacing',[element_spacing element_spacing]);
        azimuth_dbi = patternAzimuth(ura,FC,'PropagationSpeed',C);
        azimuth_slice = [az.' azimuth_dbi];
        elevation_dbi = patternElevation(ura,FC,'PropagationSpeed',C);
        elevation_slice = [az.' elevation_dbi];
        filename_az = sprintf('%d_%d_ora_uniform_az_slice.csv',j,k);
        filename_el = sprintf('%d_%d_ora_uniform_el_slice.csv',j,k);
        csvwrite(filename_az, azimuth_slice);
        csvwrite(filename_el, elevation_slice);
    end
end

    

        
    



function [pattern_phitheta, gain, phi,theta] = customPatternImport(file_path)
    % This function helperPatternImport is only in support of
    % CustomPatternExample. It may be removed in a future release.

    patternData = xlsread(file_path, 1); % import csv
 
    % Extract phi/theta values from custom pattern
     chktheta = (patternData(:,2)==patternData(1,2));
    blockLen = length(chktheta(chktheta~=0));
    nCols = size(patternData,1)/blockLen;
    thetaBlocks = reshape(patternData(:,2),blockLen,nCols);
    phiBlocks = reshape(patternData(:,1),blockLen,nCols);

    theta = thetaBlocks(1,:);
    phi = phiBlocks(:,1).';    
    gain = patternData(:,3);  
    pattern_phitheta = reshape(gain,blockLen,nCols).';      
end

function [gain, phi, theta] = customAntennaCSVImport(file_path)
    sim_csv = xlsread(file_path, 1);        
    phi = sim_csv(:, 2);
    theta = sim_csv(:, 1);    
    gain = sim_csv(:, 3);
end
