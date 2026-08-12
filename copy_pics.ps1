param(
    [string]$IP
)

$user = "rleneweaver"

# Step 1 - Move all contents from WaterMeterPics to WaterMeterPics_Archive on laptop
# Write-Host "********************Step 1: Moving local files to archive..."
# Get-ChildItem -Path "C:\RaspberryPI\WaterMeterPics" | Move-Item -Destination "C:\RaspberryPI\WaterMeterPics_Archive"

# Step 1 - Move all contents from WaterMeterPics to WaterMeterPics_Archive on laptop
Write-Host "********************Step 1: Moving local files to archive..."
Get-ChildItem -Path "C:\RaspberryPI\WaterMeterPics" -Recurse -File | ForEach-Object {
    $destPath = $_.FullName.Replace("C:\RaspberryPI\WaterMeterPics", "C:\RaspberryPI\WaterMeterPics_Archive")
    $destDir = Split-Path $destPath
    if (!(Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir | Out-Null
    }
    Move-Item -Path $_.FullName -Destination $destPath -Force
}
# Remove any empty directories left behind
Get-ChildItem -Path "C:\RaspberryPI\WaterMeterPics" -Recurse -Directory | 
    Sort-Object FullName -Descending | 
    Remove-Item

# Step 2 - Copy contents from Pi to laptop
Write-Host "********************Step 2: Copying files from Raspberry Pi to laptop..."
scp -r ${user}@${IP}:/home/rleneweaver/Pictures/watermeter/* C:\RaspberryPI\WaterMeterPics

# Step 3 - Move contents on Pi from watermeter to watermeter_archive
Write-Host "********************Step 3: Moving files on Raspberry Pi to archive..."
ssh ${user}@${IP} "cp -r /home/rleneweaver/Pictures/watermeter/* /home/rleneweaver/Pictures/watermeter_archive/ && rm -rf /home/rleneweaver/Pictures/watermeter/*"

Write-Host "Done!"
