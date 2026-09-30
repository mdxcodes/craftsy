import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive/hive.dart';
import 'package:dio/dio.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../data/models/user_profile.dart';
import '../../../data/repositories/auth_repository.dart';

/// Auth state model
class AuthState {
  final bool isAuthenticated;
  final String? userId;
  final String? phoneNumber;
  final bool isLoading;
  final UserProfile? pendingRegistration;
  final String? errorMessage;
  final int? resendCooldownSeconds;
  final String? otpRequestId;
  final bool isNewUser;

  const AuthState({
    this.isAuthenticated = false,
    this.userId,
    this.phoneNumber,
    this.isLoading = false,
    this.pendingRegistration,
    this.errorMessage,
    this.resendCooldownSeconds,
    this.otpRequestId,
    this.isNewUser = false,
  });

  AuthState copyWith({
    bool? isAuthenticated,
    String? userId,
    String? phoneNumber,
    bool? isLoading,
    UserProfile? Function()? pendingRegistration,
    String? errorMessage,
    int? resendCooldownSeconds,
    String? otpRequestId,
    bool? isNewUser,
    bool clearErrorMessage = false,
    bool clearResendCooldown = false,
    bool clearOtpRequestId = false,
  }) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      userId: userId ?? this.userId,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      isLoading: isLoading ?? this.isLoading,
      pendingRegistration: pendingRegistration != null
          ? pendingRegistration()
          : this.pendingRegistration,
      errorMessage: clearErrorMessage ? null : (errorMessage ?? this.errorMessage),
      resendCooldownSeconds: clearResendCooldown
          ? null
          : (resendCooldownSeconds ?? this.resendCooldownSeconds),
      otpRequestId: clearOtpRequestId ? null : (otpRequestId ?? this.otpRequestId),
      isNewUser: isNewUser ?? this.isNewUser,
    );
  }
}

/// Auth state notifier
class AuthNotifier extends StateNotifier<AuthState> {
  final AuthRepository _authRepository;

  AuthNotifier(this._authRepository) : super(const AuthState()) {
    _checkAuthStatus();
  }

  Future<void> _checkAuthStatus() async {
    final isAuthenticated = await _authRepository.isAuthenticated();
    final userId = await _authRepository.getUserId();
    final phoneNumber = await _authRepository.getPhoneNumber();

    state = state.copyWith(
      isAuthenticated: isAuthenticated,
      userId: userId,
      phoneNumber: phoneNumber,
    );
  }

  Future<void> signInWithPhone(String phoneNumber) async {
    state = state.copyWith(
      isLoading: true,
      pendingRegistration: () => null,
      errorMessage: null,
      resendCooldownSeconds: null,
      otpRequestId: null,
      clearOtpRequestId: true,
      isNewUser: false,
    );
    await _authRepository.savePhoneNumber(phoneNumber);
    final result = await _authRepository.requestOtp(phoneNumber);
    if (result == null) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: 'otp_send_failed'.tr(),
      );
      return;
    }
    state = state.copyWith(
      phoneNumber: phoneNumber,
      otpRequestId: result['request_id'] as String?,
      isNewUser: result['is_new_user'] as bool? ?? false,
      isLoading: false,
      errorMessage: null,
    );
  }

  Future<void> registerWithDetails(UserProfile profile) async {
    state = state.copyWith(
      isLoading: true,
      pendingRegistration: () => profile,
      phoneNumber: profile.phone,
      errorMessage: null,
      resendCooldownSeconds: null,
    );
    await _authRepository.savePhoneNumber(profile.phone);
    // Attempt registration on backend
    final backendProfile = await _authRepository.registerArtisan(profile);
    if (backendProfile != null) {
      state = state.copyWith(pendingRegistration: () => backendProfile);
    }
    state = state.copyWith(isLoading: false);
  }

  Future<bool> verifyOtp(
    String phoneNumber,
    String otp, {
    UserProfile? profileOverride,
  }) async {
    state = state.copyWith(
      isLoading: true,
      errorMessage: null,
      resendCooldownSeconds: null,
    );

    final effectivePhone = phoneNumber;
    final registrationProfile = profileOverride ?? state.pendingRegistration;
    final requestId = state.otpRequestId;

    final isNewUser = state.isNewUser;

    if (!isNewUser && registrationProfile != null && registrationProfile.id.isEmpty) {
      final regResult = await _authRepository.registerArtisan(
        registrationProfile,
      );
      if (regResult != null) {
        state = state.copyWith(pendingRegistration: () => regResult);
      }
    }

    UserProfile? backendProfile;
    String? token;
    try {
      (backendProfile, token) = await _authRepository.verifyOtpWithBackend(
        effectivePhone,
        requestId ?? '',
        otp,
      );
    } on DioException catch (e) {
      String message = 'otp_send_failed'.tr();
      if (e.response?.data is Map) {
        final detail = (e.response?.data as Map)['detail'];
        if (detail is Map) {
          message = detail['message'] as String? ?? message;
        } else if (detail is String) {
          message = detail;
        }
      } else if (e.error is String && (e.error as String).isNotEmpty) {
        message = e.error as String;
      }
      state = state.copyWith(
        isLoading: false,
        errorMessage: message,
      );
      return false;
    }

    if (backendProfile == null && token == null) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: 'otp_verification_failed'.tr(),
      );
      return false;
    }

    final currentPending = state.pendingRegistration;
    final resolvedProfile =
        backendProfile ??
        (currentPending != null
            ? currentPending.copyWith(
                id: currentPending.id.isNotEmpty
                    ? currentPending.id
                    : 'artisan_${DateTime.now().millisecondsSinceEpoch}',
                phone: effectivePhone,
              )
            : UserProfile(
                id: 'artisan_${DateTime.now().millisecondsSinceEpoch}',
                name: '',
                phone: effectivePhone,
                craftType: '',
                locationCluster: '',
                preferredLanguage: 'en',
              ));

    await _authRepository.saveAuthData(
      resolvedProfile.id,
      effectivePhone,
      token: token,
    );

    if (Hive.isBoxOpen('user_profile_box')) {
      final box = Hive.box<UserProfile>('user_profile_box');
      await box.put('current_profile', resolvedProfile);
    }

    state = state.copyWith(
      isAuthenticated: true,
      userId: resolvedProfile.id,
      phoneNumber: effectivePhone,
      isLoading: false,
      pendingRegistration: () => null,
      otpRequestId: null,
      clearOtpRequestId: true,
      isNewUser: false,
    );
    return true;
  }

  Future<void> resendOtp(String phoneNumber) async {
    state = state.copyWith(
      isLoading: true,
      errorMessage: null,
      resendCooldownSeconds: null,
      otpRequestId: null,
      clearOtpRequestId: true,
      isNewUser: false,
    );

    final result = await _authRepository.resendOtp(phoneNumber);
    state = state.copyWith(isLoading: false);

    if (result == null) {
      state = state.copyWith(
        errorMessage: 'otp_send_failed'.tr(),
      );
      return;
    }

    final cooldown = result['cooldown_seconds'] as int?;
    if (cooldown != null && cooldown > 0) {
      state = state.copyWith(
        resendCooldownSeconds: cooldown,
      );
      _startCooldown(cooldown);
      return;
    }

    state = state.copyWith(
      errorMessage: null,
      otpRequestId: result['request_id'] as String?,
    );
  }

  void _startCooldown(int seconds) {
    Future.doWhile(() async {
      if (state.resendCooldownSeconds == null) {
        return false;
      }
      await Future.delayed(const Duration(seconds: 1));
      final remaining = (state.resendCooldownSeconds ?? 1) - 1;
      if (remaining <= 0) {
        state = state.copyWith(
          resendCooldownSeconds: null,
          clearResendCooldown: true,
        );
        return false;
      }
      state = state.copyWith(resendCooldownSeconds: remaining);
      return true;
    });
  }

  void clearError() {
    state = state.copyWith(
      errorMessage: null,
      clearErrorMessage: true,
    );
  }

  Future<void> signInWithCoordinator(String coordinatorId) async {
    state = state.copyWith(isLoading: true);
    await Future.delayed(const Duration(seconds: 1));

    final userId = 'artisan_ngo_${DateTime.now().millisecondsSinceEpoch}';
    await _authRepository.saveAuthData(userId, '');
    state = state.copyWith(
      isAuthenticated: true,
      userId: userId,
      phoneNumber: '',
      isLoading: false,
      pendingRegistration: () => null,
      otpRequestId: null,
      clearOtpRequestId: true,
    );
  }

  Future<void> signOut() async {
    await _authRepository.clearAuthData();
    state = const AuthState();
  }

  Future<UserProfile?> updateProfile(UserProfile profile) async {
    state = state.copyWith(isLoading: true, errorMessage: null);
    final updated = await _authRepository.updateProfile(profile);
    if (updated != null) {
      await _authRepository.saveAuthData(
        updated.id,
        updated.phone,
        token: await _authRepository.getAccessToken(),
      );
      if (Hive.isBoxOpen('user_profile_box')) {
        final box = Hive.box<UserProfile>('user_profile_box');
        await box.put('current_profile', updated);
      }
      state = state.copyWith(
        userId: updated.id,
        phoneNumber: updated.phone,
        isLoading: false,
      );
    } else {
      state = state.copyWith(
        isLoading: false,
        errorMessage: 'profile_update_failed'.tr(),
      );
    }
    return updated;
  }
}

/// Provider for auth repository
final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository();
});

/// Provider for auth state
final authStateProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.watch(authRepositoryProvider));
});
