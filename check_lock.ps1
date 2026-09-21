$f = 'C:\Users\ROSHNI\OneDrive\Documents\GitHub\l-data-seT---ML\Comprehensive_Viva_Crop_Fertilizer_ML.pptx'
try {
    $stream = [System.IO.File]::Open($f, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::None)
    Write-Host 'Opened exclusively (no other process has it open)!'
    $stream.Close()
} catch {
    Write-Host ("Exclusively open failed: " + $_.Exception.Message)
}
