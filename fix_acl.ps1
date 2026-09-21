$path = "C:\Users\ROSHNI\OneDrive\Documents\GitHub\l-data-seT---ML"
try {
    $acl = Get-Acl -Path $path
    $acl.SetAccessRuleProtection($true, $true)
    $denyRules = @($acl.Access | Where-Object { $_.AccessControlType -eq 'Deny' })
    foreach ($rule in $denyRules) {
        $acl.RemoveAccessRule($rule) | Out-Null
        Write-Host "Removed rule: $($rule.IdentityReference) - $($rule.FileSystemRights)"
    }
    Set-Acl -Path $path -AclObject $acl
    Write-Host "SUCCESS: ACL updated on $path!"
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
}
