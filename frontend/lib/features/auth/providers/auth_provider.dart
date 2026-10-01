import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive/hive.dart';
import '../../../data/models/user_profile.dart';
import '../../../data/repositories/auth_repository.dart';
import '../../../data/services/auth_api_service.dart';

/// Auth state model
class AuthState {
  final bool isAuthenticated;
  final String? userId;
  final String? phoneNumber;
  final bool isLoading;
  final UserProfile? pendingRegistration;
  final String? errorMessage;

  const AuthState({
    this.isAuthenticated = false,
    this.userId,
    this.phoneNumber,
    this.isLoading = false,
    this.pendingRegistration,
    this.errorMessage,
  });

  AuthState copyWith({
    bool? isAuthenticated,
    String? userId,
    String? phoneNumber,
    bool? isLoading,
    UserProfile? Function()? pendingRegistration,
    String? errorMessage,
  }) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      userId: userId ?? this.userId,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      isLoading: isLoading ?? this.isLoading,
      pendingRegistration: pendingRegistration != null ? pendingRegistration() : this.pendingRegistration,
      errorMessage: errorMessage ?? this.errorMessage,
    );
  }
}

/// Auth state notifier
class AuthNotifier extends StateNotifier<AuthState> {
  final AuthRepository _authRepository;
  final AuthApiService _authApiService;

  AuthNotifier(this._authRepository, {AuthApiService? authApiService})
    : _authApiService = authApiService ?? HttpAuthApiService(),
      super(const AuthState()) {
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
    );

    try {
      final response = await _authApiService.sendOtp(phoneNumber);
      await _authRepository.savePhoneNumber(response.phone);

      state = state.copyWith(
        phoneNumber: response.phone,
        isLoading: false,
      );
    } on AuthException catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: e.message,
      );
      rethrow;
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: 'Failed to send OTP. Please try again.',
      );
      rethrow;
    }
  }

  Future<void> registerWithDetails(UserProfile profile) async {
    state = state.copyWith(
      isLoading: true,
      pendingRegistration: () => profile,
      phoneNumber: profile.phone,
    );
    await Future.delayed(const Duration(milliseconds: 500));
    await _authRepository.savePhoneNumber(profile.phone);
    state = state.copyWith(isLoading: false);
  }

  Future<bool> verifyOtp(String phoneNumber, String otp, {UserProfile? profileOverride}) async {
    state = state.copyWith(isLoading: true, errorMessage: null);

    try {
      final effectivePhone = phoneNumber.isEmpty ? '9876543210' : phoneNumber;
      final requestId = state.userId ?? '';

      final response = await _authApiService.verifyOtp(
        phone: effectivePhone,
        requestId: requestId,
        otp: otp,
      );

      await _authRepository.saveAuthData(response.artisan.id, effectivePhone);

      final registrationProfile = profileOverride ?? state.pendingRegistration;
      if (registrationProfile != null) {
        final finalProfile = registrationProfile.copyWith(
          id: response.artisan.id,
          phone: effectivePhone,
        );
        if (Hive.isBoxOpen('user_profile_box')) {
          final box = Hive.box<UserProfile>('user_profile_box');
          await box.put('current_profile', finalProfile);
        }
      }

      state = state.copyWith(
        isAuthenticated: true,
        userId: response.artisan.id,
        phoneNumber: effectivePhone,
        isLoading: false,
        pendingRegistration: () => null,
      );
      return true;
    } on AuthException catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: e.message,
      );
      return false;
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: 'Failed to verify OTP. Please try again.',
      );
      return false;
    }
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
    );
  }

  Future<void> signOut() async {
    await _authRepository.clearAuthData();
    state = const AuthState();
  }

  Future<UserProfile?> updateProfile(UserProfile profile) async {
    state = state.copyWith(isLoading: true, errorMessage: null);
    await Future.delayed(const Duration(milliseconds: 500));

    final updated = profile.copyWith(
      id: state.userId ?? profile.id,
      phone: state.phoneNumber ?? profile.phone,
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
    return updated;
  }
}

/// Provider for auth repository
final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository();
});

/// Provider for auth API service
final authApiServiceProvider = Provider<AuthApiService>((ref) {
  return HttpAuthApiService();
});

/// Provider for auth state
final authStateProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(
    ref.watch(authRepositoryProvider),
    authApiService: ref.watch(authApiServiceProvider),
  );
});
